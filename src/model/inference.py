# TODO: wait to see how to recieve the imagge from FLASK

def launch():

    img = cv2.imread(
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\test_images\ecuacion7.jpeg"
        , cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    edged = cv2.Canny(blurred, 30, 150)
    dilated = cv2.dilate(edged, (1, 1), iterations=2)
    contours = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours, bounding_boxes = sort_contours(contours, method="left-to-right")

    equation_chars = []
    for box in bounding_boxes:
        (x, y, w, h) = box

        roi = img[y:y + h, x:x + w]
        roi_binary = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        (height, width) = roi_binary.shape

        if height > width:
            roi_binary = imutils.resize(roi_binary, height=45, inter=cv2.INTER_NEAREST)
            padding = adjust_padding(int(45 - roi_binary.shape[1]))
            print(f"{roi_binary.shape} | {padding} | {width} | {height}")
            roi_binary = cv2.copyMakeBorder(roi_binary, top=0, bottom=0, left=padding[0], right=padding[1],
                                            borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))
        else:
            roi_binary = imutils.resize(roi_binary, width=45, inter=cv2.INTER_NEAREST)
            padding = adjust_padding(45 - roi_binary.shape[0])
            print(f"{roi_binary.shape} | {padding}")
            roi_binary = cv2.copyMakeBorder(roi_binary, left=0, right=0, top=padding[0], bottom=padding[1],
                                            borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255))

        equation_chars.append(roi_binary)

    index = 0
    for char in equation_chars:
        cv2.imshow(f"{index}", char)
        index += 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    equation_chars = np.array([c for c in equation_chars], dtype="float32")

    print(equation_chars)
    model = keras.models.load_model(
        r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\models\symbol_recognition_9")
    predictions = model.predict(equation_chars)
    labels = sorted(os.listdir(
        r'C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\datasets\dataset'))

    final_string = ""

    print("Pre group: ")
    print(f"Size: {len(bounding_boxes)}")
    print(bounding_boxes)
    print("===========================================")
    bounding_boxes = group_overlapped_boxes(bounding_boxes)
    print("Post group: ")
    print(f"Size: {len(bounding_boxes)}")
    print(bounding_boxes)

    for prediction, box in zip(predictions, bounding_boxes):
        x, y, w, h = box

        index = np.argmax(prediction)
        probability = prediction[index]
        label = labels[index]
        final_string += label

        print("[INFO] {} - {:.2f}%".format(label, probability*100))
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0))
        cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        cv2.imshow("Image", img)
        cv2.waitKey(0)

    print(interpret_equation_string(final_string))