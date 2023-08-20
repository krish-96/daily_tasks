function get_skeleton(movie){
  const element = document.getElementById('details');
  console.log('element style changed')
  const detail_status = document.getElementById('detail-status');
  const detail_title = document.getElementById('detail-title');
  const detail_id = document.getElementById('detail-id');
  detail_title.value = movie.title
  detail_status.value = movie.status
  detail_id.value = movie.id
  element.style.display = 'block';
};

function get_data(){}

async function details(id, req_type = "update") {
  console.log(id);
  if (req_type == "update") {
    const ticketUrl = `${window.location.origin}/ticket_detail/${id}/`
    console.log(req_type, ticketUrl);
    const response = await fetch(ticketUrl);
    const movie = await response.json();
    if (movie) {
      console.log('element has come to change style')
      get_skeleton(movie)
    }
    console.log(movie);
  } else if (req_type == "delete") {
    console.log(req_type);
    if (window.confirm("Are you sure to delete?")){
        const ticketUrl = `${window.location.origin}/ticket_delete/${id}/`
        const response = await fetch(ticketUrl);
        const movie = await response.json();
        console.log(req_type);
        window.location.reload();
    }
  }
}

function contentClose(){
    console.log('contentClose');
    const element = document.getElementById('details');
    const parentDiv = document.getElementById('detail-content');
    element.style.display = 'none';

}