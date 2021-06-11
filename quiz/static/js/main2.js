console.log('hello world quiz')
// const timerBox = document.getElementById('timer-box')
//     const time=10;
// const activateTimer = (time) => {
//     if (time.toString().length < 2) {
//         timerBox.innerHTML = `<b>0${time}:00</b>`
//     } else {
//         timerBox.innerHTML = `<b>${time}:00</b>`
//     }

//     let minutes = time - 1
//     let seconds = 10
//     let displaySeconds
//     let displayMinutes

//     const timer = setInterval(()=>{
//         seconds --
//         if (seconds < 0) {
//             seconds = 10
//             minutes --
//         }
//         if (minutes.toString().length < 2) {
//             displayMinutes = '0'+minutes
//         } else {
//             displayMinutes = minutes
//         }
//         if(seconds.toString().length < 2) {
//             displaySeconds = '0' + seconds
//         } else {
//             displaySeconds = seconds
//         }
//         if (minutes === 0 && seconds === 0) {
//             timerBox.innerHTML = "<b>00:00</b>"
//             setTimeout(()=>{
//                 clearInterval(timer)
//                 alert('Time over')
//                 sendData()
//             }, 500)
//         }

//         timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
//     }, 1000)
// }
function getanswer(){
    document.getElementById("UserAnswer").innerHTML="";
    var e=document.getElementsByTagName("input");
    for (i=0; i<=e.length;i++){
        if(e[i].type=="radio"){
            if (e[i].checked){
                document.getElementById("UserAnswer").innerHTML+="Q"+e[i].name+"The YOU select is :"+e[i].value;
            }
        }
    }
}