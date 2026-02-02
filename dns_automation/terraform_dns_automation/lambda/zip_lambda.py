# Package the lambda folder
# Only include handler.py, main.py, requirements.txt, route53_utils.py
import os
import zipfile

files_to_include = [
    'handler.py',
    'main.py',
    'requirements.txt',
    'route53_utils.py',
]
lambda_dir = os.path.dirname(os.path.abspath(__file__))
# Set zip_path to the parent directory of lambda_dir (the root of your project)
zip_path = os.path.join(os.path.dirname(lambda_dir), 'lambda.zip')

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for filename in files_to_include:
        file_path = os.path.join(lambda_dir, filename)
        if os.path.isfile(file_path):
            zipf.write(file_path, arcname=filename)

print(f"Packaged: {zip_path}")
