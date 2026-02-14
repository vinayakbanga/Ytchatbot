from PIL import Image, ImageDraw, ImageFont
import os

# Create icons directory if it doesn't exist
icon_dir = r"c:\Users\Vinayak Banga\Desktop\Ytchatbotchromeext\extension"

# Define icon sizes
sizes = [16, 48, 128]

for size in sizes:
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background (purple to blue)
    for y in range(size):
        # Calculate color gradient
        ratio = y / size
        r = int(139 + (59 - 139) * ratio)
        g = int(92 + (130 - 92) * ratio)
        b = int(246 + (246 - 246) * ratio)
        draw.rectangle([(0, y), (size, y + 1)], fill=(r, g, b, 255))
    
    # Draw rounded corners
    corner_radius = size // 4
    # Top-left
    draw.rectangle([(0, 0), (corner_radius, corner_radius)], fill=(0, 0, 0, 0))
    draw.pieslice([(0, 0), (corner_radius * 2, corner_radius * 2)], 180, 270, fill=(139, 92, 246, 255))
    # Top-right
    draw.rectangle([(size - corner_radius, 0), (size, corner_radius)], fill=(0, 0, 0, 0))
    draw.pieslice([(size - corner_radius * 2, 0), (size, corner_radius * 2)], 270, 360, fill=(139, 92, 246, 255))
    # Bottom-left
    draw.rectangle([(0, size - corner_radius), (corner_radius, size)], fill=(0, 0, 0, 0))
    draw.pieslice([(0, size - corner_radius * 2), (corner_radius * 2, size)], 90, 180, fill=(59, 130, 246, 255))
    # Bottom-right
    draw.rectangle([(size - corner_radius, size - corner_radius), (size, size)], fill=(0, 0, 0, 0))
    draw.pieslice([(size - corner_radius * 2, size - corner_radius * 2), (size, size)], 0, 90, fill=(59, 130, 246, 255))
    
    # Draw chat bubble icon
    bubble_size = int(size * 0.6)
    bubble_x = (size - bubble_size) // 2
    bubble_y = (size - bubble_size) // 2 - size // 10
    
    # Main bubble
    draw.rounded_rectangle(
        [(bubble_x, bubble_y), (bubble_x + bubble_size, bubble_y + bubble_size)],
        radius=bubble_size // 4,
        fill=(255, 255, 255, 230)
    )
    
    # Small tail
    tail_points = [
        (bubble_x + bubble_size // 3, bubble_y + bubble_size),
        (bubble_x + bubble_size // 4, bubble_y + bubble_size + bubble_size // 6),
        (bubble_x + bubble_size // 2, bubble_y + bubble_size)
    ]
    draw.polygon(tail_points, fill=(255, 255, 255, 230))
    
    # Save icon
    icon_path = os.path.join(icon_dir, f'icon{size}.png')
    img.save(icon_path, 'PNG')
    print(f'Created {icon_path}')

print('All icons created successfully!')
