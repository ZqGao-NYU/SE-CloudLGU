import defaultSettings from '@/settings'

const title = defaultSettings.title || 'Cloud LGU'

// export the page title. The title is fixed to "Cloud LGU"
// if you want to show the subtitle of each page 
//  use return `${pageTitle} - ${title}` in line 10 and comment out line 11 
export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    // return `${pageTitle} - ${title}`
    return `${title}`
  }
  return `${title}`
}
