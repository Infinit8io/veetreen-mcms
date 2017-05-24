import $ from 'jquery'
import 'geocomplete/jquery.geocomplete.min.js'
import 'bootstrap'
import 'django-formset/src/jquery.formset.js'
import './style.scss'
import Clipboard from 'clipboard/dist/clipboard.min.js'

$(() => {
    $('.with-formset').formset({
        addText: 'New item',
        addCssClass: 'btn btn-outline-primary btn-block mt-5 mb-5',
        deleteCssClass: 'btn btn-sm btn-outline-danger btn-block',
        prefix: $("#formset-prefix").val()
    })

    var mapsapi = require( 'google-maps-api' )( 'AIzaSyAqwq3SJa4X9h6fcaTpPCOjEJJhY104SkQ' , ['places'])

    mapsapi().then( function( google ) {
        $(".places-autocomplete").geocomplete()
    })

    new Clipboard('.copy')

    $(document).on('input change', '.bring-slider', function() {
        console.log($(this).val())

        let badge = $(this)
                .parents(".bring-controls-parent")
                .find(".bring-slider-value")

        badge.show()
        badge.html("I bring "+$(this).val())
    })

})
