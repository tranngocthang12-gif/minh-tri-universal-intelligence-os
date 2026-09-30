# Luật kinh nghiệm: chứng cứ và khiêm tốn — 2026-10-01

- **Trạng thái:** `UNTESTED`. Luật do Owner đặt, chưa được thử bằng vòng thật, không tự đánh dấu VERIFIED.
- **Mốc:** `main` tại `a1d06b2ce956cde419475fdc8bac55e1f5ba2d67`. Phase `FOUNDATION_PROTOTYPE`, v0.1.
- **Tính chất:** tài liệu, không đổi code. Tách biệt với `sieu-du-an`.

## Luật của Owner (nguyên văn)

LUẬT KINH NGHIỆM
1. Xem thất bại và thành công trước. Rồi mới mức trung bình.
2. Vốn/thực hành sau thạc sĩ: vừa làm vừa rút kinh nghiệm.
3. AI đôi khi sai và nói phét. Không lấy lời AI làm VERIFIED.
4. Không biết thì nói KHÔNG BIẾT. Cấm nói phét, cấm chắc hơn chứng.
5. Áp dụng ghế phản biện + mọi claim trên chat và sổ.

## Đối chiếu với lệnh đã có (ngắn, trung thực)

| Luật | Lệnh / trường đã có hỗ trợ | Lỗ (code chưa thực thi) |
| --- | --- | --- |
| 1 | `record_source` / `record_evidence` ghi được case thành công hoặc thất bại; `propose_claim.alternative` | Code **không** thực thi thứ tự "thất bại/thành công trước, rồi mới trung bình"; không có trường đánh dấu case là thành công hay thất bại |
| 2 | `set_learning_focus` (các ví dụ 10–17 ghi "sau thạc sĩ"); vòng `register_prediction` → `freeze_prediction` → `record_resolution` để rút kinh nghiệm khi làm thật | Không có cổng thời gian "sau thạc sĩ"; là quy ước của Owner |
| 3 | Không có đường nào dẫn tới `VERIFIED`; claim luôn là `HYPOTHESIS`; evidence gắn `DECLARED_UNVERIFIED`; lesson tối đa là `TRIAL_RULE` qua cổng Owner | Code không phân biệt được câu nào do AI viết so với câu do người viết |
| 4 | `propose_claim.falsifier`; trường `uncertainty` của `set_learning_focus`; `expectation_status: "UNTESTED_EXPECTATION"`; `frame_problem.unknowns` | Code **không** buộc nói "KHÔNG BIẾT" và không đo được "chắc hơn chứng"; đó là việc của ghế phản biện |
| 5 | `review_claim` / `adjudicate_claim` (critic phải khác người đề và người dự đoán theo provider ID) | Chỉ áp dụng cho claim trong sổ; trên chat là quy ước. Provider ID tự khai. Focus (`set_learning_focus`) không đi qua review |

Owner merge. Kiến trúc sư không tự merge.
