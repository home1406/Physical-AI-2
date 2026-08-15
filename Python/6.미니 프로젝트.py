import numpy as np
from tflite_runtime.interpreter import Interpreter
 
class VotingClassifier:
    """여러 경량 모델의 예측을 다수결로 결합해 신뢰도를 높인다"""
    def __init__(self, model_paths, labels):
        self.interpreters = []
        for path in model_paths:
            interp = Interpreter(model_path=path)
            interp.allocate_tensors()
            self.interpreters.append(interp)
        self.labels = labels
 
    def predict(self, image):
        votes = np.zeros(len(self.labels))
        for interp in self.interpreters:
            in_d = interp.get_input_details()[0]
            out_d = interp.get_output_details()[0]
            interp.set_tensor(in_d["index"], image)
            interp.invoke()
            probs = interp.get_tensor(out_d["index"])[0]
            votes[int(np.argmax(probs))] += 1
        winner = int(np.argmax(votes))
        confidence = votes[winner] / len(self.interpreters)
        return self.labels[winner], confidence
 
# 사용 예
# clf = VotingClassifier(["model_a.tflite", "model_b.tflite", "model_c.tflite"],
#                         labels=["정상", "불량"])
# label, conf = clf.predict(preprocessed_image)
# print(f"{label} (모델 일치도 {conf*100:.0f}%)")
