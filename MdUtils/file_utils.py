def judge_file_encoding(file_path):
    from chardet.universaldetector import UniversalDetector
    detector = UniversalDetector()
    detector.reset()
    for each in open(file_path, 'rb'):
        detector.feed(each)
        if detector.done:
            break
    detector.close()
    file_encoding = detector.result['encoding']
    confidence = detector.result['confidence']

    if confidence < 0.75:
        # 置信度过低就认为编码是 UTF-8
        file_encoding = 'utf-8'

    return file_encoding
