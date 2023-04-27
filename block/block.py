from PIL import Image
import numpy as np

def pad_image(image, block_size):
    width, height = image.size
    padded_width = ((width - 1) // block_size + 1) * block_size
    padded_height = ((height - 1) // block_size + 1) * block_size
    padded_image = Image.new(image.mode, (padded_width, padded_height), color=0)
    padded_image.paste(image, (0, 0))
    return padded_image

def split_image(image, block_size):
    width, height = image.size
    block_width = width // block_size
    block_height = height // block_size
    blocks = []
    for i in range(block_height):
        for j in range(block_width):
            box = (j * block_size, i * block_size, (j + 1) * block_size, (i + 1) * block_size)
            block = image.crop(box)
            blocks.append(np.array(block))
    return blocks

def encrypt_image(image, key, block_size):
    width, height = image.size
    encrypted_image = Image.new('RGB', (width, height), 'white')
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            block = np.array(image.crop((x, y, x + block_size, y + block_size)))
            if key.shape != (block_size, block_size):
                key = np.random.randint(0, 256, size=(block_size, block_size), dtype=np.uint8)
            key_block = key
            encrypted_block = encrypt_block(block, key_block)
            encrypted_image.paste(Image.fromarray(encrypted_block), (x, y))
    return encrypted_image

def encrypt_block(block, key):
    return np.bitwise_xor(block, key)

def encrypt_cbc(image, key, iv=None, block_size=8):
    padded_image = pad_image(image, block_size)
    
    blocks = split_image(padded_image, block_size)

    if iv is None:
        iv = np.random.randint(0, 256, size=(block_size, block_size), dtype=np.uint8)
    else:
        iv = np.array(iv, dtype=np.uint8)

    encrypted_blocks = []
    previous_block = iv
    for block in blocks:
        block_xor = np.bitwise_xor(block, previous_block)

        encrypted_block = encrypt_block(block_xor, key)

        encrypted_blocks.append(encrypted_block)

        previous_block = encrypted_block

    encrypted_image = join_blocks(encrypted_blocks)

    return encrypted_image

def join_blocks(blocks):
    block_size = blocks[0].shape[0]
    blocks_per_row = blocks_per_column = int(len(blocks) ** 0.5)

    image = Image.new('RGB', (blocks_per_row * block_size, blocks_per_column * block_size), 'white')

    for i in range(blocks_per_column):
        for j in range(blocks_per_row):
            image.paste(Image.fromarray(blocks[i * blocks_per_column + j]), (j * block_size, i * block_size))

    return image


image = Image.open('jazda.png')
key = np.random.randint(0, 256, size=(8, 8), dtype=np.uint8)
encrypted_image = encrypt_image(image, key, block_size=8)
encrypted_image.save('encrypted_image.png')

encrypted_image2 = encrypt_cbc(image, key, block_size=8)
encrypted_image2.save('encrypted_image2.png')
