let calendar_footer = document.getElementById('calendar-footer');

let days = document.querySelectorAll('.day.active');

days.forEach(day => {

    day.addEventListener('click', (evt) => {
        calendar_footer.innerHTML = evt.target.innerHTML;
    })
})

