import os
import zipfile

# Entrando na pasta 'zipados' para encontrar os arquivos .zip
os.chdir('zipados')

# Obtendo a lista de arquivos a serem descompactados
to_unzip_file_names = os.listdir()

# Descompactando cada um dos arquivos
for file_name in to_unzip_file_names:
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(f'temporary_extract/{file_name}')

# Entrando na pasta 'temporary_extract'
os.chdir('temporary_extract')

# Retirando o '.zip' que ficou no nome dos arquivos
for file_name in os.listdir():
    os.rename(file_name,file_name[:-4])