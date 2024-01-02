import copy
import os
import re
import shutil
from typing import Optional, Any

from PIL import Image

from invokeai.app.invocations.primitives import (ImageCollectionOutput,
                                                 ImageField, ImageOutput, LatentsField)
from invokeai.app.invocations.baseinvocation import (BaseInvocation, InputField, InvocationContext,
                                                     UIType, invocation, BaseInvocationOutput, Input)
from invokeai.app.services.image_records.image_records_common import ResourceOrigin, ImageCategory


@invocation("collectInOrder",
            title="Image Collection from Folder",
            version="1.0.0")
class ImagesIntoCollection(BaseInvocation):
    """Collects values into a collection"""

    collection: list[Any] = InputField(
        description="The collection, will be provided on execution", default=[], ui_hidden=True
    )

    images_input_path: str = InputField(default='', description="Absolute path and filename of input images")

    def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
        """Invoke with provided services and return outputs."""
        # Clear existing collection
        self.collection = []
        # Open the folder specified in images_input_path
        folder_path = self.images_input_path
        # Check if the folder exists

        if os.path.exists(folder_path):
            # Get a list of files in the folder
            files = os.listdir(folder_path)

            # Filter for PNG files
            png_files = [file for file in files if file.lower().endswith('.png')]
            png_files.sort()

            # Add PNG files to the collection
            for png_file in png_files:
                file_path = os.path.join(folder_path, png_file)
                loaded_image = context.services.images.get_pil_image(file_path)

                image_dto = context.services.images.create(
                    image=loaded_image,
                    image_origin=ResourceOrigin.INTERNAL,
                    image_category=ImageCategory.OTHER,
                    node_id=self.id,
                    session_id=context.graph_execution_state_id,
                    is_intermediate=self.is_intermediate,
                    # workflow = self.workflow,
                )
                self.collection.append(ImageField(image_name=image_dto.image_name))

            return ImageCollectionOutput(collection=self.collection)


@invocation("TakeImgFromFolder",
            title="Read Images From Folder",
            version="1.0.0")
class TakeImgFromFolder(BaseInvocation):
    """Collects values into a collection"""

    # item: Optional[Any] = InputField(
    #     default=None,
    #     description="The item to collect (all inputs must be of the same type)",
    #     ui_type=UIType.CollectionItem,
    #     title="Collection Item",
    #     input=Input.Connection,
    # )
    collection: list[Any] = InputField(
        description="The collection, will be provided on execution", default=[])

    images_input_path: str = InputField(default='', description="Absolute path and filename of input images")

    def invoke(self, context: InvocationContext) -> ImageCollectionOutput:
        """Invoke with provided services and return outputs."""
        # Clear existing collection
        self.collection = []
        # Open the folder specified in images_input_path
        folder_path = self.images_input_path
        # Check if the folder exists

        if os.path.exists(folder_path):
            # Get a list of files in the folder
            files = os.listdir(folder_path)

            # Filter for PNG files
            png_files = [file for file in files if file.lower().endswith('.png')]
            png_files.sort()

            png_file = None
            for file in png_files:
                if file.lower().endswith('.png'):
                    png_file = file
                    break

            processed_folder = os.path.join(folder_path, 'processed')

            if not os.path.exists(processed_folder):
                os.makedirs(processed_folder)

            # Add PNG files to the collection

            file_path = os.path.join(folder_path, png_file)
            loaded_image = context.services.images.get_pil_image(file_path)

            image_dto = context.services.images.create(
                image=loaded_image,
                image_origin=ResourceOrigin.INTERNAL,
                image_category=ImageCategory.OTHER,
                node_id=self.id,
                session_id=context.graph_execution_state_id,
                is_intermediate=self.is_intermediate,
                # workflow = self.workflow,
            )
            self.collection.append(ImageField(image_name=image_dto.image_name))
            if png_file:
                shutil.move(os.path.join(folder_path, png_file),
                            os.path.join(processed_folder, os.path.basename(png_file)))

            return ImageCollectionOutput(collection=self.collection)


@invocation("ReadSingleImage",
            title="Read single image from folder",
            version="1.0.0")
class ReadSingleImage(BaseInvocation):
    """Reads single image"""

    image: ImageField = InputField(description="Image to be passed if there is none to read")

    image_input_path: str = InputField(default='', description="Absolute path to save location")

    def invoke(self, context: InvocationContext) -> ImageOutput:
        """Invoke with provided services and return outputs."""
        # Clear existing collection
        # Open the folder specified in images_input_path
        image_to_read = self.image_input_path
        # Check if the folder exists
        if os.path.isfile(image_to_read):
            # Get a list of files in the folder
            loaded_image = context.services.images.get_pil_image(image_to_read)

            image_dto = context.services.images.create(
                image=loaded_image,
                image_origin=ResourceOrigin.INTERNAL,
                image_category=ImageCategory.OTHER,
                node_id=self.id,
                session_id=context.graph_execution_state_id,
                is_intermediate=self.is_intermediate,
                # workflow = self.workflow,
            )
            return ImageOutput(image=ImageField(image_name=image_dto.image_name),
                               width=loaded_image.width,
                               height=loaded_image.height)
        else:
            loaded_image = context.services.images.get_pil_image(self.image.image_name)
            return ImageOutput(self.image, width=loaded_image.width, height=loaded_image.height)


@invocation("SaveImageToFolder",
            title="Save Image To Folder",
            version="1.0.0")
class SaveImageToFolder(BaseInvocation):
    """Collects values into a collection"""

    # item: Optional[Any] = InputField(
    #     default=None,
    #     description="The item to collect (all inputs must be of the same type)",
    #     ui_type=UIType.CollectionItem,
    #     title="Collection Item",
    #     input=Input.Connection,
    # )

    image: ImageField = InputField(description="Image to be saved")

    images_input_path: str = InputField(default='', description="Absolute path to save location")

    def invoke(self, context: InvocationContext) -> ImageOutput:
        """Invoke with provided services and return outputs."""
        # Clear existing collection
        # Open the folder specified in images_input_path
        output_folder = self.images_input_path
        # Check if the folder exists

        if os.path.exists(output_folder):
            # Get a list of files in the folder
            PIL_image = context.services.images.get_pil_image(self.image.image_name)
            existing_images = [file for file in os.listdir(output_folder) if file.lower().endswith('.png')]
            next_number = len(existing_images) + 1
            # Save the PIL Image to the folder with the calculated number
            output_name = f"{next_number:03d}.png"  # Using three digits for the number, e.g., 001.png
            output_path = os.path.join(output_folder, output_name)
            PIL_image.save(output_path)
            return ImageOutput(image=self.image, width=PIL_image.width, height=PIL_image.height)
