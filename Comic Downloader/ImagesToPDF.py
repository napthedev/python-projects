from PIL import Image


def jpg_to_pdf(img_list, output_pdf):
    first_img = Image.open(img_list[0]).convert("RGB")
    rest = img_list[1:]
    converted = []
    for i in rest:
        converted.append(Image.open(i).convert("RGB"))
    first_img.save(output_pdf, save_all=True, append_images=converted)
