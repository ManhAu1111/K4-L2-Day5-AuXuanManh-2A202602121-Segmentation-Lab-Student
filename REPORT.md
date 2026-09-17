# Báo cáo Day 5 — điền trực tiếp trong fork của bạn

**Cách dùng:** Thay mọi dấu `…` bằng bài làm thật của bạn trước khi nộp link fork trên VLearn. Giữ nguyên bốn mục và bảng để coach đọc nhanh. Viết ngắn, cụ thể theo ảnh/vùng; không cần thuật ngữ chuyên sâu. Ví dụ trong [hướng dẫn mẫu](reports/REPORT_TEMPLATE.md) chỉ giúp hiểu cách điền, không phải câu trả lời để chép lại.

- Mã học viên theo lớp: 2A202602121 (AuXuanManh)
- Ngày / CVAT local: 17/09/2026 / http://localhost:8080
- Công cụ đã dùng: Brush / Polygon / AI model gợi ý (SegFormer & YOLOv8-seg)

Mã học viên là mã lớp cấp; không cần ghi họ tên trong report nếu kênh VLearn đã nhận diện bạn. Chỉ ghi công cụ thật sự đã dùng; không có SAM vẫn làm bài bình thường.

## 1. Bài đã nộp

Ghi tên ZIP đúng như file trong `submissions/` và số ảnh đã vẽ, Save. Chưa làm hoặc export lỗi thì ghi `chưa có`, không tạo ZIP rỗng. Cột điểm là điểm tối đa của task, **không phải điểm tự chấm**.

| Task | File ZIP đúng tên | Hoàn thành mấy ảnh | Điểm tối đa (coach chấm sau) |
| --- | --- | ---: | ---: |
| easy_semantic | easy_semantic.zip | 3 / 3 | 20 |
| medium_instance | medium_instance.zip | 3 / 3 | 32 |
| hard_panoptic | hard_panoptic.zip | 2 / 2 | 30 |
| cp1_holes | cp1_holes.zip | 1 / 1 | 3 |
| cp2_slice | cp2_slice.zip | 1 / 1 | 3 |
| cp5_occlusion | cp5_occlusion.zip | 1 / 1 | 3 |
| cp3_thin | cp3_thin.zip | 1 / 1 | 3 |
| cp4_curb | cp4_curb.zip | 1 / 1 | 3 |
| cp6_coverage | cp6_coverage.zip | 1 / 1 | 3 |
| **Tổng tối đa** | | | **100** |

Nếu export lỗi, ghi task, dữ liệu đã Save đến đâu và lỗi đã báo coach.

## 2. Một quyết định trước khi dùng gợi ý

Chọn object đầu tiên bạn tự vẽ ở `medium_instance`, trước khi xem bất kỳ đề xuất tự động nào cho object đó. Ghi ảnh/vị trí đủ để tìm lại; “quy tắc biên” là lý do bạn chọn hoặc dừng mask ở ranh đó.

- Ảnh, vị trí và object Medium đầu tiên tự vẽ: Ảnh `medium_instance` (`09f6e1f0-00000000.jpg`), xe ô tô đỗ phía bên phải đường (`car`).
- Class và quy tắc tôi dùng để chọn biên: Class `car`. Quy tắc biên: Chỉ tô phủ phần nhìn thấy của thân xe, dừng mask chính xác ở mép tiếp xúc mặt đường và không tự đoán vùng bị vật khác che.
- Nếu dùng gợi ý sau đó: Vùng gợi ý của mô hình tự động (YOLOv8-seg) bao phủ tốt 90% thân xe nhưng bị tràn nhẹ sang phần bóng râm dưới gầm xe. Tôi đã co lại mask theo đúng viền lốp và gầm xe thực tế.
- Nếu không dùng gợi ý: không dùng.

## 3. Một lỗi tôi tìm thấy và sửa

Chọn một lỗi **có thật** trong bài. Nếu công cụ lỗi khiến bạn chưa sửa được, ghi rõ đã thử gì và cần coach hỗ trợ gì; không ghi “đã sửa” khi chưa sửa.

- Task/ảnh/vùng: Task `cp2_slice`, ảnh `09f6e1f0-00001000.jpg`, vùng 2 xe ô tô đỗ sát nhau.
- Lỗi thuộc loại: gộp-tách.
- Bằng chứng tôi nhìn thấy: Gợi ý ban đầu nhập hai xe ô tô có màu tương tự đỗ cạnh nhau thành 1 mask duy nhất.
- Quy tắc và hành động sửa: Áp dụng quy tắc `cp2_slice` (hai vật cùng lớp đỗ sát nhau phải là hai instance riêng biệt), dùng Polygon/Brush chia tách thành 2 mask instance độc lập.
- Sau sửa đã Save và export lại chưa?: Đã Save và export lại ZIP `cp2_slice.zip` hợp lệ.

Nếu bạn **đã xem Summary tự đánh giá trên GitHub Actions hoặc tự chạy script**, ghi ngắn một kết quả liên quan lỗi vừa sửa (ví dụ task, metric trước/sau nếu có): Chạy `python3 scripts/inspect_submissions.py --dir submissions` xác nhận `[OK] cp2_slice: cp2_slice.zip` (annotations: 14 polygon). Scorecard ba tier tối đa **82**, không phải điểm cuối trên 100. Không tự ghi PASS/top 3/bonus; người phụ trách xác nhận theo tiêu chí lớp. Không đưa file ground truth vào fork.

## 4. Ba ca chưa chắc hoặc đã cân nhắc

Mỗi ca là một **vùng cụ thể** khiến bạn phải cân nhắc hai cách hiểu. Ghi dấu hiệu nhìn thấy hoặc quy tắc đã dùng, rồi nêu quyết định hoặc câu hỏi cho coach. Không cần ba lỗi; ca đã quyết định được cũng hợp lệ.

| Ảnh/vị trí | Hai cách hiểu có thể | Quy tắc/chứng cứ | Quyết định hoặc câu hỏi cho coach |
| --- | --- | --- | --- |
| 1. `cp4_curb` (Mép ranh giới bó vỉa) | `road` hay `sidewalk` cho vùng viền nhựa/bê tông | Ranh giới theo chức năng và bó vỉa nâng cao | Chọn `sidewalk` cho phần bó vỉa bê tông nhấc cao, và `road` cho phần mặt đường nhựa. |
| 2. `cp1_holes` (Kính xe ô tô) | Khoét rỗng kính xe hay giữ nguyên mask | Quy tắc `cp1_holes`: kính/khe hở nằm trong mask vật | Giữ nguyên phần kính chắn gió và kính cửa xe bên trong mask của `car`, không khoét rỗng. |
| 3. `cp3_thin` (Cột kim loại biển báo) | `pole` hay `background` cho cột mảnh | Cột kim loại mảnh 2-3px nổi trên nền trời | Dùng brush nhỏ (2-3px) tô chính xác nét mảnh của `pole` không bỏ sót. |
