function toggle(id) {
  var el = document.getElementById(id);
  if (el) {
    el.classList.toggle('open');
  }
}

// Initialize: expand first group, collapse others
document.addEventListener('DOMContentLoaded', function() {
  var firstGroup = document.querySelector('.nav-group-title');
  if (firstGroup) {
    firstGroup.classList.add('open');
    var firstItems = firstGroup.nextElementSibling;
    if (firstItems && firstItems.classList.contains('nav-group-items')) {
      firstItems.classList.add('open');
    }
  }
});
