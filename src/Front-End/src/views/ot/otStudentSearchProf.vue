<template>
  <div>
    <el-form label="query" style="text-align: left;margin-left:5%;margin-top:2%;">
    <el-input
      v-model="message"
      style="width: 220px"
      placeholder="Input Faculty's name"
      prefix-icon="el-icon-search"
      clearable>
    </el-input>
    <el-button @click.native=studentSearchProf()>Search</el-button>
    <el-button style="margin-left: 56%">
        <router-link to="/officetime/student/my" >My Reservations</router-link>
    </el-button>
    </el-form>
    <div v-if="loading">dsa</div>
      <div v-else>    <p style="margin-left:35%; font-size:2rem;">{{ message }}'s Office Time</p>
        <div style="margin-left:5%; width:90%;">

    <FullCalendar
      :options="calendarOptions"
    />
        </div></div>
  </div>
</template>

<script>
import '@fullcalendar/core/vdom'
import FullCalendar from '@fullcalendar/vue'
import DayGridPlugin from '@fullcalendar/daygrid'
import TimeGridPlugin from '@fullcalendar/timegrid'
import InteractionPlugin from '@fullcalendar/interaction'
import ListPlugin from '@fullcalendar/list'
import { bookOfficeTime, searchProf } from '@/api/ot'

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
      value: '',
      message: '',
      loading: true,
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
            booked_by: 'student'
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
        height:660,
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: false,
          hour12: false // 设置时间为24小时
        },
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
        selectable: false,
        events: []
      }
    }
  },
  created () {
    this.message = this.$route.params.message
    this.studentSearchProf()
  },
  methods: {
    studentSearchProf: function () {
      if (this.message==''){this.loading = true}
      // alert('send'+this.message)
   searchProf(this.message)
    .then(res => {
      if (res.data['success']){
        this.loading = false
        alert('success')
        this.$message({
          message: 'Search Successfully',
          type: 'success'
        })
        this.calendarOptions.events = []
        console.log('here')
        console.log(res.data)
        for (var i = 0; i < res.data['slots'].length; i++) {
          // if (!this.source.otLists[i].isBooked) {
            this.calendarOptions.events.push({
              id: res.data['slots'][i]['otID'],
              title: 'Office Time',
              start: res.data['slots'][i]['otDate'] + 'T' + res.data['slots'][i]['otStartTime'],
              end: res.data['slots'][i]['otDate'] + 'T' + res.data['slots'][i]['otEndTime'],
              backgroundColor: '#b0e0e6',
              overlap: false,
              extendedProps: {
                Location: res.data['slots'][i]['otLocation']
              }
            })
          // } else {
          //   this.calendarOptions.events.push({
          //     id: this.source.otLists[i].otID.toString(),
          //     title: 'Office Time',
          //     start: this.source.otLists[i].otDate + 'T' + this.source.otLists[i].otStartTime + ':00',
          //     end: this.source.otLists[i].otDate + 'T' + this.source.otLists[i].otEndTime + ':00',
          //     overlap: true,
          //     extendedProps: {
          //       Location: this.source.otLists[i].otLocation
          //     }
          //   })
          // }
        }

      } else{
        this.$alert("Create post fail!")
      }
    })
    .catch(function (error) { // 请求失败处理
      console.log(error);
    })
      
    },
    // handleDateClick: function (arg) {
    //   let dateStr = arg.dateStr.substring(0, 10)
    //   let startStr = arg.dateStr.substring(11, 16)
    //   if (confirm('您是否要在' + dateStr + ' ' + startStr + '添加Office Time?')) {
    //     var length = prompt('Enter minutes in format like 20')
    //     var startTime = new Date(dateStr + 'T' + startStr + ':00')
    //     var endTime = new Date(startTime.setMinutes(startTime.getMinutes() + parseInt(length)))
    //     this.calendarOptions.events.push({
    //       id: '3',
    //       title: 'Office Time',
    //       start: arg.dateStr,
    //       end: endTime,
    //       s: '#b0e0e6',
    //       overlap: false,
    //       extendedProps: {
    //         Location: 'proplace'
    //       }
    //     })
    //   }
    // },
    handleButtonClick: function () {
      var dateStr = prompt('Enter a date in format 2022-04-01')
      var startStr = prompt('Enter start time in format 10:00')
      var endStr = prompt('Enter end time in format 22:00')
      var startTime = new Date(dateStr + 'T' + startStr + ':00')
      var endTime = new Date(dateStr + 'T' + endStr + ':00')

      if (!isNaN(startTime.valueOf())) { // valid?
        this.calendarOptions.events.push({
          id: '4',
          title: 'dynamic event',
          start: startTime,
          end: endTime
        })
        alert('Great. Now, update your database...')
      } else {
        alert('Invalid date.')
      }
    },
    handleEventClick: function (info) {
      // alert(info.event.extendedProps.Location)
      if (!info.event.overlap) {
        if (confirm('您是否要预约' + info.event.start + '的Office Time?')) {
            var student_id=this.$store.state.user.token
              bookOfficeTime(info.event.id, student_id)
    .then(res => {
      if (res.data['success']){
        this.$message({
          message: 'Search Successfully',
          type: 'success'
        })
          this.calendarOptions.events.push({
            id: info.event.id,
            title: info.event.title,
            start: info.event.start,
            end: info.event.end,
            overlap: true,
            extendedProps: {
              Location: info.event.extendedProps.Location
            }
          })
          let index = this.calendarOptions.events.findIndex(e => e.id === info.event.id)
          this.calendarOptions.events.splice(index, 1)
      } else{
        this.$alert("Create post fail!")
      }
    })
    .catch(function (error) { // 请求失败处理
      console.log(error);
    })
        }
      }
    },
    handleMouseEnter: function (info) {
      // alert('Event: ' + info.event.title)
      tippy(info.el, {
        content: info.event.extendedProps.Location
      })
    }
  }
}
</script>

<style>
</style>
