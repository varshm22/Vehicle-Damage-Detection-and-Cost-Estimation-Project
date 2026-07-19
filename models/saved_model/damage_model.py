"""
Damage Detection Model using YOLOv8
"""

from ultralytics import YOLO
import os


class DamageDetectionModel:
    def __init__(self):
        """
        Initialize and load trained YOLO model
        """
        model_path = os.path.join("models", "best.pt")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")

        self.model = YOLO(model_path)

        # Class names (must match your trained model)
        self.class_names = {
            0: "dent",
            1: "scratch",
            2: "crack",
            3: "glass shatter",
            4: "lamp broken",
            5: "tire flat"
        }

        print("✅ YOLOv8 Damage Model Loaded Successfully")


    def predict_damage(self, image_path):
        """
        Detect all damages in image using YOLOv8
        """

        print("🔥 YOLO MODEL IS RUNNING 🔥")

        results = self.model(image_path)

        detections = []

        if len(results[0].boxes) == 0:
            return []

        for box in results[0].boxes:
            class_id = int(box.cls)
            confidence = float(box.conf)

            damage_type = self.class_names.get(class_id, "unknown")

            # Estimate severity from confidence
            if confidence > 0.8:
                severity = "high"
            elif confidence > 0.5:
                severity = "medium"
            else:
                severity = "low"

            detections.append({
                "damage_type": damage_type,
                "severity": severity,
                "confidence": round(confidence, 2)
            })

        return detections


    def calculate_total_cost(self, detections, car_category):
        """
        Realistic repair cost estimation in INR
        Based on damage type, severity, and car category
        """

        # Base costs for ECONOMY car in INR
        cost_map = {
            "dent": 4000,
            "scratch": 2500,
            "crack": 7000,
            "glass shatter": 12000,
            "lamp broken": 4500,
            "tire flat": 5000
        }

        # Car category multiplier
        category_multiplier = {
            "economy": 1.0,
            "mid-range": 1.6,
            "premium": 2.8
        }

        total_cost = 0

        for d in detections:
            base_cost = cost_map.get(d["damage_type"], 3000)

            # Severity multiplier
            if d["severity"] == "high":
                severity_multiplier = 1.6
            elif d["severity"] == "medium":
                severity_multiplier = 1.3
            else:
                severity_multiplier = 1.0

            total_cost += base_cost * severity_multiplier

        # Apply car category multiplier
        category_factor = category_multiplier.get(car_category, 1.0)

        final_cost = total_cost * category_factor

        return int(final_cost)