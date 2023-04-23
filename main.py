import patterns
import display
import numpy as np
import masks
import common
import reed_solomon as rs

"""
TODO:
- déterminer automatiquement le nb d'erreurs
- disposer les données en blocks pour les QR codes plus grands.
"""


def bin_qr(binData, quality):

    # Determine best size
    charCount = np.ceil(binData.bit_length() / 8)
    minVersion = 0
    offset = 2
    for i in range(40):
        if i >= 10:
            offset = 3
        if (common.get_qr_properties(i + 1, quality)[0] - offset) >= charCount:
            minVersion = i + 1
            break

    if minVersion == 0:
        print("Too much data to fit in a QR code with this quality!\nTry using a lower quality")
        return None
    
    print("Minimal version:", minVersion)

    # Add byte mode
    charCountSize = 0
    if minVersion < 10:
        charCountSize = 8
        capacityOffset = 2
    else:
        charCountSize = 16
        capacityOffset = 3

    capacity, errCount, (grp1Size, grp1BlockSize), (grp2Size, grp2BlockSize) = common.get_qr_properties(minVersion, quality)
    maxSize = (capacity - capacityOffset) * 8
    print(errCount)

    binData = (0b0100 << int(charCount * 8 + charCountSize)) | (int(charCount) << int(charCount * 8)) | binData

    diff = maxSize - binData.bit_length()
    if diff > 4:
        #Todo add padding after terminator
        terminatorSize = int(((charCount * 8 + charCountSize + 4) % 8))
        totalSize = charCount * 8

        diff2 = int((maxSize - totalSize) // 8)
        binData = binData << terminatorSize

        for i in range(diff2):
            if i % 2 == 0:
                binData = (binData << 8) | 236
            else:
                binData = (binData << 8) | 17

    dataArray = common.bin_to_array(binData)
    dataArray.reverse()

    rs.init_tables()

    group1Data = []
    group1EC = []
    group2Data = []
    group2EC = []
    for i in range(grp1Size):
        encodedMsg = rs.rs_encode_msg(dataArray[i*grp1BlockSize:(i+1)*grp1BlockSize], errCount)
        group1Data.append(encodedMsg[:grp1BlockSize])
        group1EC.append(encodedMsg[grp1BlockSize:])
    for i in range(grp2Size):
        encodedMsg = rs.rs_encode_msg(dataArray[i*grp2BlockSize:(i+1)*grp2BlockSize], errCount)
        group2Data.append(encodedMsg[:grp2BlockSize])
        group2EC.append(encodedMsg[grp2BlockSize:])

    interleavedData = []
    for i in range(max(grp1BlockSize, grp2BlockSize)):
        if i < grp1BlockSize:
            for j in range(grp1Size):
                interleavedData.append(group1Data[j][i])
                #print("G1", j, i)

        if i < grp2BlockSize:
            for j in range(grp2Size):
                interleavedData.append(group2Data[j][i])
                #print("G2", j, i)

    interleavedEC = []
    for i in range(errCount):
        for j in range(grp1Size):
            interleavedEC.append(group1EC[j][i])

        for j in range(grp2Size):
            interleavedEC.append(group2EC[j][i])

    interleavedCodewords = interleavedData + interleavedEC

    dataStream = common.bytearray_to_bin(interleavedCodewords)

    #print(bin(dataStream))

    dataMatrix = place_data(minVersion, dataStream, (capacity + errCount * (grp1Size + grp2Size)) * 8)

    #display.show_matrix(dataMatrix, showAxis=True)

    mask = choose_mask(minVersion, quality, dataMatrix)
    M = patterns.add_padding(mask_data(minVersion, dataMatrix, mask) | generate_patterns(minVersion, quality, mask), 4, 4, 4, 4)

    return M


def generate_patterns(version, errorCorrection, mask):
    patternMatrix = np.bitwise_or(
        np.bitwise_or(
            np.bitwise_or(
                patterns.generate_finder_patterns(version), 
                patterns.generate_alignment_patterns(version)
            ),
            np.bitwise_or(
                patterns.generate_timing_patterns(version),
                patterns.generate_dark_module(version)
            )
        ),
        np.bitwise_or(
            patterns.generate_version_info(version),
            patterns.generate_format_info(version, errorCorrection, mask)
        )
    )

    return patternMatrix

def place_data(version, data, dataSize):
    size = (version - 1) * 4 + 21
    reserved = patterns.generate_reserved_areas(version)

    D = np.zeros((size, size), dtype=np.uint8)

    directionUp = True
    lastMoveHorizontal = False
    posX = size-1
    posY = size-1
    count = 0
    t = ""
    while count < dataSize:
        if posX >= 0 and not reserved[posY, posX] == 1:
            
            D[posY, posX] = (((data & (0b1 << (dataSize - count - 1))) >> (dataSize - count - 1)) + 0b0)
            #print(data.bit_length(), (0b1 << (dataSize - count)).bit_length())
            t+= str(((data & (0b1 << (dataSize - count - 1))) >> (dataSize - count - 1)))
            """
            D[posY, posX] = (data & 0b1) + 0b0
            t+= str(data & 0b1)
            data = data >> 1
            """
            count = count + 1

        #print(dataSize, count)
        #print(posX, posY)

        if lastMoveHorizontal:
            lastMoveHorizontal = False
            posX = posX + 1
            if directionUp:
                posY = posY - 1
            else:
                posY = posY + 1
        else:
            lastMoveHorizontal = True
            posX = posX - 1

        if posY < 0:
            posY = 0
            posX = posX - 2
            if posX == 6:
                posX = 5
            directionUp = False
        elif posY >= size:
            posY = size - 1
            posX = posX - 2
            if posX == 6:
                posX = 5
            directionUp = True

        if posX < -1:
            raise IndexError("Trop de données pour ce format")
            #print("Trop de données pour ce format !")
            #print(count, count / 8)
            #print(bin(data))
    
    #print("t:", t)
    return D


def choose_mask(version, errorCorrection, dataMatrix):
    size = (version - 1) * 4 + 21
    penalties = []
    for i in range(8):
        M = mask_data(version, dataMatrix, i)

        QR = np.logical_or(generate_patterns(version, errorCorrection, i), M)

        #display.show_matrix(QR)

        penalty = 0

        # Penalty rule nb 1:
        # Check in each row (and column) if there is a block of at least five
        # consecutive modules that are the same color
        for i in range(size):
            colCount = 0
            colLastBit = 0
            rowCount = 0
            rowLastBit = 0

            for j in range(size):
                if colLastBit == QR[i, j]:
                    colCount = colCount + 1
                    if colCount == 5:
                        penalty = penalty + 3
                    elif colCount > 5:
                        penalty = penalty + 1
                else:
                    colCount = 0
                    colLastBit = QR[i, j]

                if rowLastBit == QR[j, i]:
                    rowCount = rowCount + 1
                    if rowCount == 5:
                        penalty = penalty + 3
                    elif rowCount > 5:
                        penalty = penalty + 1
                else:
                    rowCount = 0
                    rowLastBit = QR[j, i]

        # Penalty rule nb 2:
        # Check if there are 2x2 blocks where all 4 modules are the same color
        for i in range(size-1):
            for j in range(size-1):
                if QR[i, j] & QR[i+1, j] & QR[i, j+1] & QR[i+1, j+1]:
                    penalty = penalty + 3

        # Penalty rule nb 3:
        # Check for dark-light-dark-dark-dark-light-dark patterns that have 4
        # light modules on either side
        for i in range(size):
            for j in range(size - 11):
                col = common.array_to_bin(QR[i, j:j+11])
                row = common.array_to_bin(QR[i, j:j+11])
                if col == 0b10111010000 or col == 0b00001011101:
                    penalty = penalty + 40
                if row == 0b10111010000 or row == 0b00001011101:
                    penalty = penalty + 40
        
        # Penalty rule nb 4:
        # Calculate the dark-to-light ratio
        dark = np.count_nonzero(QR == 1)
        percentage = (dark / (size * size)) * 100

        prev = (percentage // 5) * 5
        next = prev + 5

        prevScore = np.abs(prev - 50) / 5
        nextScore = np.abs(next - 50) / 5

        penalty = penalty + min(prevScore, nextScore) * 10

        penalties.append(penalty)

    bestMask = penalties.index(min(penalties))

    return bestMask

def mask_data(version, dataMatrix, mask):
    size = (version - 1) * 4 + 21
    reserved = patterns.generate_reserved_areas(version)

    M = np.zeros((size, size))

    maskFun = masks.MASK_FUNCTIONS[mask]

    for i in range(size):
        for j in range(size):
            if maskFun(i, j):
                M[i, j] = 1

    MM = np.logical_and(M, np.logical_xor(reserved, np.ones((size, size))))

    return np.logical_xor(dataMatrix, MM)


msg = common.conversion_entier("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla pharetra dapibus sapien, id sollicitudin augue ullamcorper quis. Morbi id condimentum tortor. Sed finibus ligula risus, at fringilla ex sollicitudin dapibus. Vestibulum non erat tempus, gravida risus ut, sodales diam. Etiam tristique hendrerit posuere. Proin sagittis libero quam, et mattis ex finibus a. Donec varius urna ac sollicitudin pellentesque. Donec at sapien et magna auctor porta. Donec tristique erat a velit feugiat hendrerit eget quis enim. Proin sit amet mollis eros. Sed rutrum vel dui in blandit. Vestibulum ex ligula, accumsan a lacinia ut, porttitor eget eros. Vestibulum nunc quam, sagittis sed dignissim in, venenatis quis sapien. Nulla facilisi.")
common.array_to_bin(msg)

display.show_matrix(bin_qr(common.bytearray_to_bin(msg), 'M'))

#display.save_matrix(bin_qr(common.bytearray_to_bin(msg), 'M'), 'qr.png')