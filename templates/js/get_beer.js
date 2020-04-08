$(document).ready(function(){

    function showError(error){
        $('#success').html('');
        $('#error').html(error);
    }


    function check_height(e) {
        // Если появляется скролл и его ширина больше клиентской → увеличиваем ширину клиента
        if (this.scrollHeight > this.clientHeight) {
            this.style.height = this.scrollHeight + 5 + 'px';
        }
    }

    function send_data(e) {
        data = JSON.parse($(`#${this.dataset.id}`).val())
        data.item_id = data._id
        $.ajax({
            dataType: 'json',
            url: '/beerblog/save_beer',
            type: 'POST',
            data: JSON.stringify(data),
            success: function(data) {
                console.log(data)
            }
        })
    }

    function save_new_item() {
        data = JSON.parse($(`#new_item_json`).val())
        $.ajax({
            dataType: 'json',
            url: '/beerblog/save_item',
            type: 'POST',
            data: JSON.stringify(data),
            success: function(data) {
                console.log(data)
            }
        })

    }

    $('#save_new_item').on('click', save_new_item)

    showBeer1 = () => {
        $.ajax({
            dataType: 'json',
            url: '/beerblog/get_beer?page=1',
            type: 'POST',
            // data: JSON.stringify({'page': page}),
            success: function(data) {

                for (beer of data.beer){
                    $('#beer_container').append(`


                        <form role="form" style="width:100%">

                            <div class="form-group row">

                                <textarea id="${beer['_id']}" class="json_items" style="width:7000px">${JSON.stringify(beer, undefined, 2)}</textarea>
                            </div>


                            <input class="btn btn-primary submit" title="Сохранить" type="button" data-id="${beer['_id']}" value="Сохранить">
                            <input class="btn btn-danger delete" title="Удалить" type="button" data-id="${beer['_id']}" value="Удалить">
                            <div class="form-group"></div>
                            <hr>
                        </form>`);
                }




                pag = data.pagination
                if (pag.page <= 1) {
                    $('#prev_link').attr('class', 'disabled')
                }
                if (!pag.has_next) {
                    $('#next_link').attr('class', 'disabled')
                }
                $('#prev_link').attr('page', pag.prev)
                $('#next_link').attr('page', pag.next)

                $('.json_items').map(check_height)

                $('.json_items').on('input', check_height)

                $('.submit').on('click', send_data)
                $('.json_items').on('input', check_height)
            }
        })
    }




    showBeer1()

    $('.get_beer_btn').on('click', function(e){
        e.preventDefault()
        console.log(this.attributes.page.value)
        page = this.attributes.page.value
        $.ajax({
            dataType: 'json',
            url: `/beerblog/get_beer?page=${page}`,
            // url: url,
            type: 'POST',
            // data: JSON.stringify({'page': page}),
            success: function(data) {

                for (beer of data.beer){
                    $('#beer_container').append(`
                        <div class="row">
                            <input>
                                ${JSON.stringify(beer, undefined, 2)}
                            </input>
                        </div>`);
                }   

                pag = data.pagination
                console.log(pag)
                if (pag.page <= 1) {
                    $('#prev_link').attr('class', 'disabled')
                } else {
                    $('#prev_link').removeAttr('class', 'disabled')
                }
                if (!pag.has_next) {
                    $('#next_link').attr('class', 'disabled')
                } else {
                    $('#next_link').removeAttr('class', 'disabled')
                }
                $('#prev_link').attr('page', pag.prev)
                $('#next_link').attr('page', pag.next)
            }
        })
    })

})