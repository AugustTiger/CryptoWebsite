import json
import os

# Đọc dữ liệu từ projects.json
with open("projects.json", "r", encoding="utf-8") as f:
    projects = json.load(f)

# Đọc template HTML
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# Tạo thư mục projects nếu chưa tồn tại
os.makedirs("projects", exist_ok=True)

# Sinh file HTML cho mỗi dự án
for project in projects:
    # Xử lý requirements
    requirements_html = "".join(
        f'<li><strong>{req["label"]}:</strong> {req["value"]}</li>'
        for req in project["requirements"]
    )

    # Xử lý instructions
    instructions_html = ""
    counter = 1  # Biến đếm số thứ tự
    is_first_ol = True  # Theo dõi xem có đang trong <ol> đầu tiên không

    for instr in project["instructions"]:
        if isinstance(instr, dict):
            # Đóng <ol> nếu đang mở
            if not is_first_ol:
                instructions_html += "</ol>"
            # Thêm div cho ảnh
            instructions_html += (
                '<div style="text-align: center;">'
                f'<img src="../images/{instr["image"]}" alt="{instr["alt"]}" style="max-width: 100%; height: auto;" />'
                f'<p style="font-style: italic; color: #666; font-size: 0.9em; margin-top: 5px; margin-bottom: 0;">{instr["caption"]}</p>'
                '</div>'
            )
            # Mở <ol> mới với số bắt đầu phù hợp
            instructions_html += f'<ol start="{counter}">'
            is_first_ol = False
        else:
            # Nếu là mục đầu tiên hoặc sau ảnh, mở <ol> nếu cần
            if is_first_ol:
                instructions_html += '<ol>'
                is_first_ol = False
            instructions_html += f"<li>{instr}</li>"
            counter += 1  # Tăng số thứ tự chỉ khi thêm mục văn bản

    # Đóng <ol> cuối cùng nếu đang mở
    if not is_first_ol:
        instructions_html += "</ol>"

    # Thay thế placeholder
    content = template.format(
        title=project["title"],
        date=project["date"],
        description=project["description"],
        main_image=project["main_image"],
        requirements=requirements_html,
        instructions=instructions_html,
        learn_more_url=project["learn_more_url"]
    )

    # Tạo tên file
    filename = project["title"].lower().replace("airdrop dự án ", "").replace(" ", "_") + ".html"
    filepath = os.path.join("projects", filename)

    # Chỉ ghi file nếu chưa tồn tại
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Đã sinh: {filepath}")
    else:
        print(f"Bỏ qua: {filepath} đã tồn tại")

# Sinh project_list.json (luôn ghi đè để cập nhật danh sách mới)
project_list = [
    {
        "id": project["id"],
        "title": project["title"],
        "date": project["date"],
        "image": f"images/{project['main_image']}",
        "shortDesc": project["description"],
        "detailsUrl": f"projects/{project['title'].lower().replace('airdrop dự án ', '').replace(' ', '_')}.html"
    }
    for project in projects
]

with open("project_list.json", "w", encoding="utf-8") as f:
    json.dump(project_list, f, ensure_ascii=False, indent=4)
print("Đã sinh: project_list.json")