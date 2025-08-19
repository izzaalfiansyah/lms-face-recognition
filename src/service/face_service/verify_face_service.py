import face_recognition


def verify_face(image) -> int:
    image_local = "src/assets/gibran.jpg"

    print("search image", image)
    print("local image", image_local)

    image1 = face_recognition.load_image_file(image_local)
    image1_encoding = face_recognition.face_encodings(image1)[0]

    image2 = face_recognition.load_image_file(image)
    image2_encoding = face_recognition.face_encodings(image2)[0]

    results = face_recognition.compare_faces([image1_encoding], image2_encoding)
    distances = face_recognition.face_distance([image1_encoding], image2_encoding)

    print(distances[0])
    print(results[0])

    return 1
