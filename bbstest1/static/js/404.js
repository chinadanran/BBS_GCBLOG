var myCanvas = document.getElementById("canvas");
myCanvas.style.height = window.innerHeight + 'px';
var canvas = myCanvas.getContext("2d");
var starObj = new Image();
starObj.src = "http://www.jq22.com/img/cs/300x500-1.png";
var starArr = [];
var cw = myCanvas.width;
var ch = myCanvas.height;
var starNum;

function a() {
    window.history.go(-1);
}
//创建星星的类
function Star(x, y, w, h, img, speedY, speedX) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.img = img; //星星图片
    this.speedY = speedY; //星星Y速度
    this.speedX = speedX; //星星X速度
    this.rx = 0; //星星的图片位置
};
//星星运动动画
Star.prototype.move = function() {
    this.y += this.speedY;
    this.x += this.speedX;
    canvas.drawImage(this.img, this.rx, 0, this.w, this.h, this.x, this.y, this.w, this.h)
}

function animat() {
    //清除画板，每清除一次，运动一次，实现运动的假象
    //把像素推进去
    canvas.clearRect(0, 0, cw, ch);
    //游戏主函数
    main();
    //动画函数  每一帧执行一次
    window.requestAnimationFrame(animat)
}
//入口
animat();

function main() {
    starNum = rand(0, 100);
    if (starNum < 50) {
        var x1 = rand(0, cw + 1000);
        var speedy = rand(2, 4); //一种速度
        var speedx = rand(3, 4); //另一种速度
        starArr.push(new Star(x1, -76, 64, 76, starObj, speedy, -speedy));
        starArr.push(new Star(x1, -76, 64, 76, starObj, speedx, -speedx));
        //召唤星星
    }
    if (starNum < 5) {
        var speedz = rand(5, 8);
        starArr.push(new Star(x1, -76, 64, 76, starObj, speedz, -speedz));
    }
    if (starNum < 2) {
        var speedv = rand(12, 14);
        starArr.push(new Star(x1, -76, 64, 76, starObj, speedv, -speedv));
    }
    for (var i = 0; i < starArr.length; i++) {
        starArr[i].move();
        if (starArr[i].y > ch || starArr[i].x < 0) {
            starArr.splice(i, 1);
        }
    }

}

function rand(min, max) {
    return parseInt(Math.random() * (max - min + 1) + min);
}