import pytesseract
from PIL import Image
for i in range(50,51):
    imageUrl = f"C:\\Users\\Decade\\Desktop\\demo\\{i}.jpeg";
    image = Image.open(imageUrl,"r");
    print(image)
    text = pytesseract.image_to_string(image,lang="jpn");

    contexts = str(text).split();
    with open(imageUrl.replace("jpeg", "txt"), 'w', encoding="UTF-8") as output:
        index = 1;
        for context in contexts:
            if index % 5 == 0:
                output.write("\n")
            index += 1;
            output.write(context);
        print("写入完成!");
