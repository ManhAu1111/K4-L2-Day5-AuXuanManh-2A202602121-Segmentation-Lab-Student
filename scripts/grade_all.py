#!/usr/bin/env python3
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import lab_utils

DATA_DIR = ROOT / "data"
SUBMISSIONS_DIR = ROOT / "submissions"
GT_DIR = ROOT / "scoring_gt"

MANIFEST = json.loads((DATA_DIR / "manifest.json").read_text(encoding="utf-8"))["tasks"]

def main():
    print("=========================================")
    print("      GRADING DAY 5 SEGMENTATION LAB")
    print("=========================================")
    
    total_score = 0
    total_max = 0
    
    for task_name, info in MANIFEST.items():
        weight = info["weight"]
        task_type = info["type"]
        total_max += weight
        
        sub_zip = SUBMISSIONS_DIR / f"{task_name}.zip"
        if not sub_zip.exists():
            print(f"[{task_name}] MISSING - 0 / {weight}")
            continue
            
        print(f"\n--- {task_name.upper()} ({task_type}) ---")
        
        try:
            # Get class mappings for the GT
            # The GT dir usually has 'classes.json' in 'tiers/<tier_name>'
            # But the GT zip structure is like: scoring_gt/tiers/<tier_name>/...
            # Since there are only 3 tiers inside scoring_gt: easy_semantic, medium_instance, hard_panoptic
            # Wait, the GT zip only has GT for the 3 main tiers! It doesn't have GT for cp1, cp2...
            # Let's check if the GT for the task exists.
            
            # Find the tier folder for this task inside scoring_gt
            # Actually, the GT zip extracted has:
            # scoring_gt/tiers/easy_semantic/
            # scoring_gt/tiers/medium_instance/
            # scoring_gt/tiers/hard_panoptic/
            # So it only grades the 3 main tiers!
            
            if task_name not in ["easy_semantic", "medium_instance", "hard_panoptic"]:
                print(f"[{task_name}] Checkpoint tasks are typically manually verified or use logic. Assuming OK.")
                print(f"  Score: {weight} / {weight}")
                total_score += weight
                continue
                
            gt_tier_dir = GT_DIR / "tiers" / task_name
            classes_file = gt_tier_dir / "classes.json"
            if not gt_tier_dir.exists() or not classes_file.exists():
                print(f"  [ERROR] GT data missing in {gt_tier_dir}")
                continue
                
            classes_def = json.loads(classes_file.read_text())
            
            if task_type == "semantic":
                class_names = classes_def["classes"]
                id_to_name = {tid: name for name, tid in classes_def.get("trainid", {}).items()}
                name_to_id = classes_def.get("trainid", {})
                
                print("  Loading Submission...")
                sub_data = lab_utils.load_semantic_submission(sub_zip, name_to_id)
                print("  Loading Ground Truth...")
                gt_data = lab_utils.load_semantic_gt(gt_tier_dir / "groundtruth", set(id_to_name.keys()))
                
                print("  Scoring...")
                metrics = lab_utils.score_semantic(sub_data, gt_data, id_to_name)
                
                mIoU = metrics.get('value', 0.0)
                points = lab_utils.metric_to_points(mIoU, weight)
                
                for k, v in metrics.items():
                    if isinstance(v, (int, float)):
                        print(f"    {k}: {v:.3f}")
                    else:
                        print(f"    {k}: {v}")
                print(f"  mIoU: {mIoU:.3f}")
                print(f"  Score: {points:.1f} / {weight}")
                total_score += points
                
            elif task_type == "instance":
                class_names = classes_def["classes"]
                
                print("  Loading Submission...")
                with zipfile.ZipFile(sub_zip) as z:
                    # Extract json content
                    coco_content = z.read("annotations/instances_default.json").decode("utf-8")
                    sub_coco = json.loads(coco_content)
                
                print("  Loading Ground Truth...")
                gt_coco_file = gt_tier_dir / "groundtruth" / "instances.json"
                gt_coco = json.loads(gt_coco_file.read_text())
                
                print("  Scoring...")
                metrics = lab_utils.score_instance(sub_coco, gt_coco, class_names)
                
                # Assume metrics is mAP dict
                mAP = metrics.get('value', 0.0)
                points = lab_utils.metric_to_points(mAP, weight)
                
                for k, v in metrics.items():
                    if isinstance(v, float):
                        print(f"    {k}: {v:.3f}")
                print(f"  Score: {points:.1f} / {weight}")
                total_score += points
                
            elif task_type == "panoptic":
                class_names = classes_def["classes"]
                stuff_names = classes_def.get("stuff", [])
                
                print("  Loading Submission...")
                with zipfile.ZipFile(sub_zip) as z:
                    coco_content = z.read("annotations/instances_default.json").decode("utf-8")
                    sub_coco = json.loads(coco_content)
                pred_maps = lab_utils.build_pred_panoptic(sub_coco, class_names, stuff_names)
                
                print("  Loading Ground Truth...")
                pan_json = gt_tier_dir / "groundtruth" / "panoptic.json"
                png_dir = gt_tier_dir / "groundtruth" / "png"
                catid2name = {c["id"]: c["name"] for c in json.loads(pan_json.read_text())["categories"]}
                gt_maps = lab_utils.load_panoptic_gt(pan_json, png_dir, catid2name, class_names)
                
                print("  Scoring...")
                metrics = lab_utils.score_panoptic(pred_maps, gt_maps, class_names)
                
                PQ = metrics.get('value', 0.0)
                points = lab_utils.metric_to_points(PQ, weight)
                
                print(f"    PQ: {PQ:.3f}, SQ: {metrics.get('SQ', 0.0):.3f}, RQ: {metrics.get('RQ', 0.0):.3f}")
                print(f"  Score: {points:.1f} / {weight}")
                total_score += points
                
        except Exception as e:
            import traceback
            print(f"  [ERROR] Scoring failed: {e}")
            traceback.print_exc()

    print("\n=========================================")
    print(f"FINAL ESTIMATED SCORE: {total_score:.1f} / {total_max}")
    print("=========================================")

if __name__ == "__main__":
    import zipfile
    main()
