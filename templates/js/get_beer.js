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
    $('.json_items').map(check_height)

    function send_data(e) {
        data = JSON.parse($(`#${this.dataset.id}`).val())
        data.item_id = data._id
        delete data._id
        data.collection = this.dataset.collection
        data.db = this.dataset.db
        $.ajax({
            dataType: 'json',
            url: '/save_item',
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

    function get_collection(e) {
        e.preventDefault()
        collection = this.dataset.collection
        db = this.dataset.db
        data = {
            'db': this.dataset.db,
            'collection': this.dataset.collection
        }
        $.ajax({
            dataType: 'json',
            url: '/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data) {
                $('#fields').empty()
                $('#items_container').empty()
                for (let li of data.fields){
                    $('#fields').append(`<button id=field_${li} class="field btn btn-outline-primary list-group-item">${li}</button>`)
                }
                $('.field').on('click', choose_field)


                for (item of data.items){
                    $('#items_container').append(`


                        <form role="form" style="width:100%">

                            <div class="form-group row">

                                <textarea id="${item['_id']}" class="json_items" style="width:7000px">${JSON.stringify(item, undefined, 2)}</textarea>
                            </div>


                            <input class="btn btn-primary submit" title="Сохранить" type="button" data-id="${item['_id']}" data-db="${db}" data-collection="${collection}" value="Сохранить">
                            <input class="btn btn-danger delete" title="Удалить" type="button" data-id="${item['_id']}" data-db="${db}" data-collection="${collection}" value="Удалить">
                            <div class="form-group"></div>
                            <hr>
                        </form>`);
                }




                pag = data.pagination
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
                $('#prev_link').attr('collection', collection)
                $('#prev_link').attr('db', db)
                $('#next_link').attr('page', pag.next)
                $('#next_link').attr('collection', collection)
                $('#next_link').attr('db', db)

                $('.json_items').map(check_height)

                $('.json_items').on('input', check_height)

                $('.submit').on('click', send_data)
                $('.json_items').on('input', check_height)
            }
        });
    }

    function choose_field(e) {
        elem = $(`#${this.id}`)
        if (elem.hasClass('btn-outline-primary')) {
            elem.removeClass('btn-outline-primary')
            elem.addClass('btn-primary')
            elem.css('background-color', '#007bff')
        } else {
            elem.removeClass('btn-primary')
            elem.addClass('btn-outline-primary')
            elem.css('background-color', '')
        }
    }

    function show_hide_collection(e) {
        if ($(`#${this.dataset.database}`).css('display') == 'none') {
            $(`#${this.dataset.database}`).css('display', 'block')
        } else {
            $(`#${this.dataset.database}`).css('display', 'none') 
        }
    }

    $('#save_new_item').on('click', save_new_item)
    $('.collections').on('click', get_collection)
    $('.databases').on('click', show_hide_collection)


    // showBeer1 = (data) => {
    //     $.ajax({
    //         dataType: 'json',
    //         url: '/beerblog/get_beer?page=1',
    //         type: 'POST',
    //         // data: JSON.stringify({'page': page}),
    //         success: function(data) {

    //             for (beer of data.beer){
    //                 $('#beer_container').append(`


    //                     <form role="form" style="width:100%">

    //                         <div class="form-group row">

    //                             <textarea id="${beer['_id']}" class="json_items" style="width:7000px">${JSON.stringify(beer, undefined, 2)}</textarea>
    //                         </div>


    //                         <input class="btn btn-primary submit" title="Сохранить" type="button" data-id="${beer['_id']}" value="Сохранить">
    //                         <input class="btn btn-danger delete" title="Удалить" type="button" data-id="${beer['_id']}" value="Удалить">
    //                         <div class="form-group"></div>
    //                         <hr>
    //                     </form>`);
    //             }




    //             pag = data.pagination
    //             if (pag.page <= 1) {
    //                 $('#prev_link').attr('class', 'disabled')
    //             } else {
    //                 $('#prev_link').removeAttr('class', 'disabled')
    //             }
    //             if (!pag.has_next) {
    //                 $('#next_link').attr('class', 'disabled')
    //             } else {
    //                 $('#next_link').removeAttr('class', 'disabled')
    //             }
    //             $('#prev_link').attr('page', pag.prev)
    //             $('#next_link').attr('page', pag.next)

    //             $('.json_items').map(check_height)

    //             $('.json_items').on('input', check_height)

    //             $('.submit').on('click', send_data)
    //             $('.json_items').on('input', check_height)
    //         }
    //     })
    // }




    // showBeer1()

    $('.get_beer_btn').on('click', function(e){
        e.preventDefault()
        collection = this.attributes.collection.value
        data = {
            'db': this.attributes.db.value,
            'collection': collection,
            'page': this.attributes.page.value
        }
        $.ajax({
            dataType: 'json',
            url: '/get_data',
            type: 'POST',
            data: JSON.stringify(data),
            processData: false,
            contentType: false,
            success: function(data) {
                $('#fields').empty()
                $('#items_container').empty()
                for (let li of data.fields){
                    $('#fields').append(`<button id=field_${li} class="field btn btn-outline-primary list-group-item">${li}</button>`)
                }
                $('.field').on('click', choose_field)


                for (item of data.items){
                    $('#items_container').append(`


                        <form role="form" style="width:100%">

                            <div class="form-group row">

                                <textarea id="${item['_id']}" class="json_items" style="width:7000px">${JSON.stringify(item, undefined, 2)}</textarea>
                            </div>


                            <input class="btn btn-primary submit" title="Сохранить" type="button" data-id="${item['_id']}" data-db="${db}" data-collection="${collection}" value="Сохранить">
                            <input class="btn btn-danger delete" title="Удалить" type="button" data-id="${item['_id']}" data-db="${db}" data-collection="${collection}" value="Удалить">
                            <div class="form-group"></div>
                            <hr>
                        </form>`);
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

                $('.json_items').map(check_height)

                $('.json_items').on('input', check_height)

                $('.submit').on('click', send_data)
                $('.json_items').on('input', check_height)
            }
        })
    })

})