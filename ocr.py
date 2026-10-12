from paddleocr import PaddleOCR
import re

def recognize_chat(roi):
    ocr = PaddleOCR(
        lang="ch",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        enable_mkldnn=False
    )
    width = roi.shape[1]
    center = width / 2
    result = ocr.predict(roi)
    messages = []
    max_gap = 15
    for page in result:
        texts = page["rec_texts"]
        boxes = page["rec_boxes"]

        # 按照文字的纵坐标排序
        lines = sorted(
            zip(texts, boxes),
            key=lambda item: item[1][1]
        )

        last_sender = None
        last_bottom = None

        for text, box in lines:
            x1, y1, x2, y2 = box
            cx = (x1 + x2) / 2

            # 过滤时间戳
            is_time = re.fullmatch(
                r"\d{1,2}:\d{2}", text.strip()
            )

            if is_time and abs(cx - center) < width * 0.15:
                last_sender = None
                last_bottom = None
                continue

            # 判断发送方
            sender = "我" if cx > center else "对方"

            # 计算和上一行的距离
            if last_bottom is not None:
                gap = y1 - last_bottom
            else:
                gap = float("inf")

            # 判断能否合并
            if (
                    sender == last_sender
                    and 0 <= gap <= max_gap
            ):
                messages[-1]["text"] += text
            else:
                messages.append({
                    "sender": sender,
                    "text": text
                })

            last_sender = sender
            last_bottom = y2

    return messages