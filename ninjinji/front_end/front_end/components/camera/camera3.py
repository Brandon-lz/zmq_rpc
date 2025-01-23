import reflex as rx

# id是摄像头的id，必须从0开始
def create(id:str="0",width:str="300px",height:str="230px",style:dict={}) -> rx.Component:    
    return rx.html(
        f"""
<video id="videoElement{id}" autoplay></video>
        """,
        on_mount=rx.call_script(
            """
navigator.mediaDevices.enumerateDevices()
  .then(devices => {
    const videoDevices = devices.filter(device => device.kind === 'videoinput');
    const videoStreams = videoDevices.map(device => {
      //console.log(device.deviceId);
      return navigator.mediaDevices.getUserMedia({ video: { deviceId: device.deviceId } });
    });
    
    Promise.all(videoStreams)
      .then(streams => {
        // 处理每个视频流
        streams.map((stream,index) => {
          console.log(stream,index);
          if (index!="""+id+"""){
            return
          }
          // 在页面上显示视频流
         //const videoElement = document.createElement('video');
          const videoElement = document.getElementById('videoElement'+index);
          //console.log(videoElement);
          videoElement.srcObject = stream;
          console.log("摄像头：",index);
        //   document.body.appendChild(videoElement);
        });
      })
      .catch(error => {
        console.error('Error accessing video streams:', error);
      });
  })
  .catch(error => {
    console.error('Error enumerating video devices:', error);
  });

            """
        ),
        width=width,  # 设置大小
        height = height,
        # max_height="201px",
        transform="scaleX(-1);",  # 左右对称翻转
        border_width = "0.5em",
        style = style
    )
        # padding_top="3em",
       
