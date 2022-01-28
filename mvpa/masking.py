"""Mask .nii files with anatomical maps."""
from pathlib import Path
import yaml
from nilearn.masking import intersect_masks, apply_mask
from nilearn.image import load_img, resample_img


class MVPAMasker:
    """Class that handles masking of images with anatomical masks."""

    def __init__(self):
        self.mask_defs = self.get_mask_defs()

    def load_mask(self, mask_name):
        """Return an intersected mask image based on named mask definitions."""
        return intersect_masks(self.mask_defs[mask_name], threshold=0,
                               connected=False)

    def apply_mask(self, img_list, mask_name):
        """Apply mask to list of images and return masked images."""
        img = load_img(img_list)

        # resample mask to ensure same affine as images
        mask_res = resample_img(self.load_mask(mask_name),
                                target_affine=img.affine,
                                target_shape=img.shape[:3],
                                interpolation='nearest')

        return apply_mask(img, mask_res)

    @staticmethod
    def get_mask_defs():
        """Load YAML mask definition file and return contents as dict."""
        project_root = Path(__file__).parents[1]
        filename = project_root / 'mask_defs.yaml'
        with open(filename, encoding="utf-8") as file:
            return yaml.safe_load(file)
