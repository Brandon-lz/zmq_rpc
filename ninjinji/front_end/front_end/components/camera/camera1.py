import reflex as rx

def create(max_width:str="500px") -> rx.Component:
    return rx.vstack(
        rx.html(
        """
<video id="videoElement" autoplay></video>
        """,
        on_mount=rx.call_script(
            """
// 获取video元素
var video = document.getElementById('videoElement');

// 检查浏览器是否支持WebRTC
if (navigator.mediaDevices.getUserMedia) {
// 请求访问摄像头
navigator.mediaDevices.getUserMedia({ video: true })
.then(function (stream) {
    // 将视频流绑定到video元素
    video.srcObject = stream;
})
.catch(function (error) {
    console.log('访问摄像头出错: ' + error);
});
} else {
console.log('抱歉，你的浏览器不支持WebRTC');
}
            """
        ),
        max_width=max_width,  # 设置大小
        height="auto",
        transform="scaleX(-1);",  # 左右对称翻转
        ),
        # padding_top="3em",
    )
