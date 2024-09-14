document.getElementById('codeForm').addEventListener('submit', function(event) {
  event.preventDefault();

  const code = encodeURIComponent(document.getElementById('codeInput').value);

  fetch('/?code=' + code).then(_ => { location.reload() })
});
