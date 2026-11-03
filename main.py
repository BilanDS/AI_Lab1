
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Відкриваємо GeoTIFF
with rasterio.open("scene.tif") as src:
    print("Система координат:", src.crs)
    print("Розмір зображення:", src.width, "x", src.height)

    gsd_x, gsd_y = src.res
    print(f"GSD по X: {gsd_x:.4f} м/піксель")
    print(f"GSD по Y: {gsd_y:.4f} м/піксель")

    scene_width = src.width * gsd_x
    scene_height = src.height * gsd_y

    print(f"Ширина сцени: {scene_width:.2f} м")
    print(f"Висота сцени: {scene_height:.2f} м")
    print(f"Площа сцени: {scene_width * scene_height / 10000:.2f} га")

    rgb = src.read([1, 2, 3])

# Перетворюємо канали для відображення
image = np.moveaxis(rgb, 0, -1)

# Відображаємо знімок
plt.figure(figsize=(12, 10))
plt.imshow(image)
plt.title("RGB ортофотоплан")
plt.axis("off")
plt.show()

# Гістограми каналів RGB
plt.figure(figsize=(10, 6))

for band, color, name in zip(rgb, ["red", "green", "blue"],
                             ["Red", "Green", "Blue"]):
    plt.hist(band.ravel(), bins=100, histtype="step",
             color=color, label=name)

plt.xlabel("Значення пікселя")
plt.ylabel("Кількість пікселів")
plt.title("Гістограми каналів RGB")
plt.legend()
plt.grid()
plt.show()

# Вимірювання
fig, ax = plt.subplots(figsize=(14, 10))
ax.imshow(image)
ax.set_title("Вимірювання: 1. Наблизьте (Zoom) | 2. Вимкніть Zoom | 3. Клацніть 2 точки")
ax.axis("on")

coords = []

def onclick(event):
    toolbar = plt.get_current_fig_manager().toolbar
    if event.button == 1 and event.inaxes and toolbar.mode == '':
        coords.append((event.xdata, event.ydata))
        ax.plot(event.xdata, event.ydata, 'ro')
        fig.canvas.draw()
        
        # Коли зібрано дві точки, проводимо лінію і рахуємо відстань
        if len(coords) == 2:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            
            pixels = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            meters = pixels * gsd_x
            
            print(f"Виміряно об'єкт: {pixels:.1f} пікселів | Розмір: {meters:.2f} м")
            
            ax.plot([x1, x2], [y1, y2], "y-", linewidth=2)
            fig.canvas.draw()
            coords.clear()

# Підключаємо обробник подій до графіка
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()