import patterns
import display
import numpy as np
import masks
import common

def generate_patterns(version, errorCorrection, mask):
    patternMatrix = np.logical_or(
        np.logical_or(
            np.logical_or(
                patterns.generate_finder_patterns(version), 
                patterns.generate_alignment_patterns(version)
            ),
            np.logical_or(
                patterns.generate_timing_patterns(version),
                patterns.generate_dark_module(version)
            )
        ),
        np.logical_or(
            patterns.generate_version_info(version),
            patterns.generate_format_info(version, errorCorrection, mask)
        )
    )

    return patternMatrix

def choose_mask(version, errorCorrection, dataMatrix):
    size = (version - 1) * 4 + 21
    penalties = []
    for i in range(8):
        M = mask_data(version, dataMatrix, i)

        QR = np.logical_or(generate_patterns(version, errorCorrection, i), M)

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

for i in range(8):
    mask_data(8, None, i)

