import numpy as np


class ApertureExtractor:
    @staticmethod
    def from_boolean_mask(boolean_mask, column, row):
        """
        Returns the aperture pixels coordinates for the given boolean mask.
        @param boolean_mask: the boolean mask centered in the given column and row.
        @param column: the center column of the mask.
        @param row: the center row of the mask.
        @return: the pixels columns and rows in an array.
        """
        boolean_mask = np.transpose(boolean_mask)
        # TODO resize pipeline_mask to match
        pipeline_mask_triceratops = np.zeros((len(boolean_mask), len(boolean_mask[0]), 2))
        for i in range(0, len(boolean_mask)):
            for j in range(0, len(boolean_mask[0])):
                pipeline_mask_triceratops[i, j] = [column + i, row + j]
        pipeline_mask_triceratops[~boolean_mask] = None
        aperture = []
        for i in range(0, len(pipeline_mask_triceratops)):
            for j in range(0, len(pipeline_mask_triceratops[0])):
                if not np.isnan(pipeline_mask_triceratops[i, j]).any():
                    aperture.append(pipeline_mask_triceratops[i, j])
        return aperture

    @staticmethod
    def from_pixels_to_boolean_mask(aperture_pixels, column, row, col_len, row_len):
        boolean_mask = np.full((row_len, col_len), False)
        for i in range(row, row + row_len):
            for j in range(column, column + col_len):
                if isinstance(aperture_pixels[0], np.ndarray):
                    boolean_mask[i - row][j - column] = any(([j, i] == x).all() for x in aperture_pixels)
                else:
                    boolean_mask[i - row][j - column] = any(([j, i] == x) for x in aperture_pixels)
        return boolean_mask

