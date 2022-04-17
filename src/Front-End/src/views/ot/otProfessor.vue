<template>
  <div>
    <!-- <el-form label="query" style="text-align: left">
    <el-input
      v-model="message"
      style="width: 220px"
      placeholder="Input Professor's name"
      prefix-icon="el-icon-search"
      clearable>
    </el-input>
    <el-button @click.native=studentCheckOT()>查询</el-button>
    </el-form> -->
    <p style="margin-left:42%; margin-top:3%; font-size:2rem;">{{ source.Professor_Name }}'s Office Time</p>
    <div style="margin-left:5%; width:90%;">
    <FullCalendar
      :options="calendarOptions"
    />
    </div>
  </div>
</template>

<script>
import '@fullcalendar/core/vdom'
import FullCalendar from '@fullcalendar/vue'
import DayGridPlugin from '@fullcalendar/daygrid'
import TimeGridPlugin from '@fullcalendar/timegrid'
import InteractionPlugin from '@fullcalendar/interaction'
import ListPlugin from '@fullcalendar/list'

// import axios from 'axios'
import tippy from 'tippy.js'
// import 'tippy.js/dist/tippy.css'
// import 'tippy.js/themes/light.css';
// import 'tippy.js/animations/scale.css';

// require('@fullcalendar/core/main.min.css')
require('@fullcalendar/daygrid/main.min.css')
require('@fullcalendar/timegrid/main.min.css')

export default {
  components: {FullCalendar},
  data () {
    return {
      message: 'prof1',
      source: {
        Professor_Name: 'p1',
        success: true,
        otLists:
        [
          {
            otID: 11,
            otDate: '2022-04-10',
            otStartTime: '09:00',
            otEndTime: '10:00',
            otLocation: 'place1',
            isBooked: false,
            booked_by: ''
          },
          {
            otID: 12,
            otDate: '2022-04-11',
            otStartTime: '09:00',
            otEndTime: '10:00',
            otLocation: 'place1',
            isBooked: true,
            booked_by: 'student'
          }
        ]
      },
      calendarOptions: {
        plugins: [ DayGridPlugin, InteractionPlugin, TimeGridPlugin, ListPlugin ],
        initialView: 'timeGridWeek',
        // backgroundColor: '#D3D3D3',
        headerToolbar: { // 日历头部按钮位置
          left: 'title',
          center: '',
          right: 'prev today next'
        },
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: false,
          hour12: false // 设置时间为24小时
        },
        height: 660,
        customButtons: {
          addEventButton: {
            text: 'add event...',
            click: this.handleButtonClick
          }
        },
        slotDuration: '00:10:00',
        slotMaxTime: '24:00:00',
        slotMinTime: '8:00:00',
        allDaySlot: false,
        dateClick: this.handleDateClick,
        eventClick: this.handleEventClick,
        eventMouseEnter: this.handleMouseEnter,
        selectable: true,
        events: []
      }
    }
  },
  created () {
    if (!this.source.success) {
      alert('cannot find')
    } else {
      this.calendarOptions.events = []
      this.message = this.source.Professor_Name
      for (var i = 0; i < this.source.otLists.length; i++) {
        if (!this.source.otLists[i].isBooked) {
          this.calendarOptions.events.push({
            id: this.source.otLists[i].otID.toString(),
            title: 'Office Time',
            start: this.source.otLists[i].otDate + 'T' + this.source.otLists[i].otStartTime + ':00',
            end: this.source.otLists[i].otDate + 'T' + this.source.otLists[i].otEndTime + ':00',
            backgroundColor: '#b0e0e6',
            overlap: false,
            extendedProps: {
              Location: this.source.otLists[i].otLocation,
              booked_by: this.source.otLists[i].booked_by
            }
          })
        } else {
          this.calendarOptions.events.push({
            id: this.source.otLists[i].otID.toString(),
            title: 'Office Time',
            start: this.source.otLists[i].otDate + 'T' + this.source.otLists[i].otStartTime + ':00',
            end: this.source.otLists[i].otDate + 'T' + this.source.otLists[i].otEndTime + ':00',
            overlap: true,
            extendedProps: {
              Location: this.source.otLists[i].otLocation,
              booked_by: this.source.otLists[i].booked_by
            }
          })
        }
      }
    }
  },
  methods: {
    handleDateClick: function (arg) {
      let dateStr = arg.dateStr.substring(0, 10)
      let startStr = arg.dateStr.substring(11, 16)
      if (confirm('您是否要在' + dateStr + ' ' + startStr + '添加Office Time?')) {
        var length = prompt('Enter minutes in format like 20')
        var location = prompt('Enter the location')
        var startTime = new Date(dateStr + 'T' + startStr + ':00')
        var endTime = new Date(startTime.setMinutes(startTime.getMinutes() + parseInt(length)))
        this.calendarOptions.events.push({
          id: '3',
          title: 'Office Time',
          start: arg.dateStr,
          end: endTime,
          backgroundColor: '#b0e0e6',
          overlap: false,
          extendedProps: {
            Location: location
          }
        })
      }
    },
    handleEventClick: function (info) {
      // alert(info.event.extendedProps.Location)
      if (confirm('您是否要删除' + info.event.start + '的Office Time?')) {
        let index = this.calendarOptions.events.findIndex(e => e.id === info.event.id)
        this.calendarOptions.events.splice(index, 1)
      }
    },
    handleMouseEnter: function (info) {
      if (info.event.overlap) {
        tippy(info.el, {
          content: info.event.extendedProps.Location + ',   booked by: ' + info.event.extendedProps.booked_by
        })
      } else {
        tippy(info.el, {
          content: info.event.extendedProps.Location
        })
      }
    }
  }
}
</script>

<style>
</style>
