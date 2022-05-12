<template>
  <div class="dashboard-container">
    <img src="@/assets/home.png" alt="" width="100%" height="100%">
  </div>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  // Home page
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name',
      'roles'
    ])
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
