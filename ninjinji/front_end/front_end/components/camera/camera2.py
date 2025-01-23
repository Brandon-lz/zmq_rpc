import reflex as rx

class CameraState(rx.State):
    # 用于存储拍摄的图片（Base64 格式）
    image_data: str = ""

    def save_image(self, data: str):
        """保存拍摄的图像数据"""
        self.image_data = data

def create():
    return rx.box(
        rx.divider(),
        rx.text("Camera Feed", font_size="1.5em"),
        rx.box(
            # 包含摄像头预览和拍照按钮
            rx.html("""
                <div style="text-align:center;">
                    <video id="video" width="320" height="240" autoplay></video>
                    <canvas id="canvas" width="320" height="240" style="display:none;"></canvas>
                    <button id="snap">Take Photo</button>
                </div>
                <script>
                    const video = document.getElementById("video");
                    const canvas = document.getElementById("canvas");
                    const snapButton = document.getElementById("snap");
                    const context = canvas.getContext("2d");

                    // 开启摄像头
                    navigator.mediaDevices.getUserMedia({ video: true })
                        .then(stream => {
                            video.srcObject = stream;
                            video.play();
                        })
                        .catch(err => {
                            console.error("Error accessing camera:", err);
                        });

                    // 拍照并发送数据
                    snapButton.addEventListener("click", () => {
                        context.drawImage(video, 0, 0, canvas.width, canvas.height);
                        const imageData = canvas.toDataURL("image/png");
                        window.rx.call("save_image", imageData); // 调用 Reflex 状态方法
                    });
                </script>
            """),
            style={"textAlign": "center"}
        ),
        rx.divider(),
        # 显示拍摄的照片
        rx.cond(
            CameraState.image_data,
            rx.image(src=CameraState.image_data, width="320px", height="240px"),
            rx.text("No photo captured yet.")
        )
    )