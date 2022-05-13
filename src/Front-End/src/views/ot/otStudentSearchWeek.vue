<template>
  <div>
    <el-form label="query" style="text-align: left;margin-left:5%;margin-top:2%;">
      <el-input
        v-model="message"
        style="width: 220px"
        placeholder="Input Faculty's name"
        prefix-icon="el-icon-search"
        clearable
      />
      <el-button>
        <router-link :to="{name:'studentSearchProf', params:{message: message}}">Search</router-link>
      </el-button>
      <el-button style="margin-left: 63%">
        <router-link to="/officetime/student/my"> My Reservations</router-link>
      </el-button>
    </el-form>
    <p style="margin-left:35%; font-size:2rem;">Available Office Time</p>
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
import { searchWeek } from '@/api/ot'
require('@fullcalendar/daygrid/main.min.css')
require('@fullcalendar/timegrid/main.min.css')

export default {
  components: { FullCalendar },
  data() {
    return {
      message: 'prof1',
      calendarOptions: { //settings for imported fullCalendar
        plugins: [DayGridPlugin, InteractionPlugin, TimeGridPlugin, ListPlugin],
        initialView: 'dayGridWeek',
        headerToolbar: {
          left: 'title',
          center: '',
          right: 'prev today next'
        },
        height: 660,
        slotLabelFormat: {
          hour: '2-digit',
          minute: '2-digit',
          meridiem: false,
          hour12: false
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
  created() {
    // show available profs this week
    searchWeek()
      .then(res => {
        if (res.data['success']) {
          this.$message({
            message: 'Search Successfully',
            type: 'success'
          })
          this.calendarOptions.events = []
          for (var key in res.data['lists']) {
            for (var j = 0; j < res.data['lists'][key].length; j++) {
              this.calendarOptions.events.push({
                id: 1,
                title: key + "'s Office Time",
                start: res.data['lists'][key][j],
                allDay: true,
                overlap: true,
                extendedProps: {
                  prof_name: key
                }
              })
            }
          }
        } else {
          this.$alert('No available OfficeTime this week!')
        }
      })
      .catch(function(error) { // request failure error
        console.log(error)
      })
  },
  methods: {
    // click a professor jump to his page
    handleEventClick: function(info) {
      this.$router.push({
        name: 'studentSearchProf',
        params: { message: info.event.extendedProps.prof_name }
      })
    }
  }
}
</script>

<style>
</style>
