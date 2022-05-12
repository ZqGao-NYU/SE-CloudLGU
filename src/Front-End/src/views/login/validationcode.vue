<template>
  <div class="s-canvas">
    <canvas id="s-canvas" :width="contentWidth" :height="contentHeight" />
  </div>
</template>
<script>
export default {
  name: 'ValidationCode',
  props: {
    identifyCode: { // default code
      type: String,
      default: '1234'
    },
    fontSizeMin: { // minimum font size
      type: Number,
      default: 25
    },
    fontSizeMax: { // maximum font size
      type: Number,
      default: 35
    },
    backgroundColorMin: { // minimum color number of the background
      type: Number,
      default: 200
    },
    backgroundColorMax: { // maximum color number of the background
      type: Number,
      default: 220
    },
    dotColorMin: { // minimum color number of the dots
      type: Number,
      default: 60
    },
    dotColorMax: { // maximum color number of the dots
      type: Number,
      default: 120
    },
    contentWidth: { // width
      type: Number,
      default: 90
    },
    contentHeight: { // height
      type: Number,
      default: 38
    }
  },
  watch: {
    identifyCode() {
      this.drawPic()
    }
  },
  mounted() {
    this.drawPic()
  },
  methods: {
  // random number
    randomNum(min, max) {
      return Math.floor(Math.random() * (max - min) + min)
    },

    // random color
    randomColor(min, max) {
      const r = this.randomNum(min, max)
      const g = this.randomNum(min, max)
      const b = this.randomNum(min, max)
      return 'rgb(' + r + ',' + g + ',' + b + ')'
    },

    drawPic() {
      const canvas = document.getElementById('s-canvas')
      const ctx = canvas.getContext('2d')
      ctx.textBaseline = 'bottom'
      // draw the background
      ctx.fillStyle = '#e6ecfd'
      ctx.fillRect(0, 0, this.contentWidth, this.contentHeight)
      // draw the text
      for (let i = 0; i < this.identifyCode.length; i++) {
        this.drawText(ctx, this.identifyCode[i], i)
      }
      this.drawLine(ctx)
      this.drawDot(ctx)
    },

    drawText(ctx, txt, i) {
      ctx.fillStyle = this.randomColor(50, 160) // random color of the text
      ctx.font = this.randomNum(this.fontSizeMin, this.fontSizeMax) + 'px SimHei' // random size of the text
      const x = (i + 1) * (this.contentWidth / (this.identifyCode.length + 1))
      const y = this.randomNum(this.fontSizeMax, this.contentHeight - 5)
      var deg = this.randomNum(-30, 30)
      // change origin point and rotate
      ctx.translate(x, y)
      ctx.rotate(deg * Math.PI / 180)
      ctx.fillText(txt, 0, 0)
      // restore origin point
      ctx.rotate(-deg * Math.PI / 180)
      ctx.translate(-x, -y)
    },

    drawLine(ctx) {
      // draw intefereing lines
      for (let i = 0; i < 4; i++) {
        ctx.strokeStyle = this.randomColor(100, 200)
        ctx.beginPath()
        ctx.moveTo(this.randomNum(0, this.contentWidth), this.randomNum(0, this.contentHeight))
        ctx.lineTo(this.randomNum(0, this.contentWidth), this.randomNum(0, this.contentHeight))
        ctx.stroke()
      }
    },

    drawDot(ctx) {
      // draw interfering dots
      for (let i = 0; i < 30; i++) {
        ctx.fillStyle = this.randomColor(0, 255)
        ctx.beginPath()
        ctx.arc(this.randomNum(0, this.contentWidth), this.randomNum(0, this.contentHeight), 1, 0, 2 * Math.PI)
        ctx.fill()
      }
    }
  }
}
</script>
