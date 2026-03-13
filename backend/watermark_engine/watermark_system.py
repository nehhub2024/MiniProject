# # from datetime import datetime
# # from PIL import Image

# # class WatermarkSystem:

# #      def embed(self, input_path, output_path, user_hash, image_id, signature_path):
# #         image = Image.open(input_path)
# #         image.save(output_path)
# #         timestamp = str(datetime.now())
# #         watermark_seed = f"{user_hash}_{image_id}_{timestamp}"
# #         return watermark_seed, timestamp

# #      def decode(self, suspicious_path):
# #         # Placeholder decode logic
# #         # Replace with real extraction later
# #         return "fake_extracted_seed"



# from datetime import datetime
# from PIL import Image


# class WatermarkSystem:

#     def embed(self, input_path, output_path, user_hash, image_id, signature_path):
#         """
#         Temporary placeholder watermark embedding.
#         Later replace with DWT-DCT-SVD algorithm.
#         """

#         # Open original image
#         image = Image.open(input_path)

#         # Save watermarked image (currently just copy)
#         image.save(output_path)

#         # Generate watermark seed
#         timestamp = str(datetime.now())
#         watermark_seed = f"{user_hash}_{image_id}_{timestamp}"

#         return watermark_seed, timestamp


#     def decode(self, suspicious_path):
#         """
#         Temporary placeholder watermark decoding.
#         Later replace with real watermark extraction.
#         """

#         try:
#             # Open suspicious image
#             image = Image.open(suspicious_path)

#             # Convert to RGB just to ensure image loads
#             image = image.convert("RGB")

#             # Fake extracted seed (for testing)
#             extracted_seed = "fake_extracted_seed"

#             return extracted_seed

#         except Exception as e:
#             raise Exception(f"Decode failed: {str(e)}")



from datetime import datetime
from PIL import Image


class WatermarkSystem:

    def embed(self, input_path, output_path, user_hash, image_id, signature_path):
        """
        Temporary placeholder watermark embedding.
        Replace with real algorithm later.
        """

        # Open original image
        image = Image.open(input_path)

        # Save watermarked image (just copy)
        image.save(output_path)

        # Generate watermark seed
        timestamp = str(datetime.now())
        watermark_seed = f"{user_hash}_{image_id}_{timestamp}"

        return watermark_seed, timestamp


    def decode(self, suspicious_path):
        """
        Temporary placeholder watermark decoding.
        Replace with real extraction later.
        """

        try:
            image = Image.open(suspicious_path)
            image = image.convert("RGB")

            extracted_seed = "fake_extracted_seed"

            return extracted_seed

        except Exception as e:
            raise Exception(f"Decode failed: {str(e)}")