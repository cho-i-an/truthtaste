$(document).ready(function () {
    var ajax_url = $('#create-review').attr('data-ajax-url');
    var store_id = $('#create-review').attr('data-store-id');
    console.log(ajax_url)
    console.log(store_id)

    $('.review-form').on('submit', function (event) {
        event.preventDefault();

        var data = {
            'rating': $('input[name="rating"]:checked').val(),
            'title': $('input[name="title"]').val(),
            'content': $('textarea[name="content"]').val(),
            'author': $('input[name="author"]').val(),
            'store_id': store_id
        }
        console.log(data)
        $.ajax({
            url: ajax_url,
            type: 'POST',
            data: {
                'rating': $('input[name="rating"]:checked').val(),
                'title': $('input[name="title"]').val(),
                'content': $('textarea[name="content"]').val(),
                'author': $('input[name="author"]').val(),
                'store_id': store_id
            },
            dataType: 'json',
            context: this,
            headers: {"X-CSRFToken": csrftoken}

        }).done(function (json) {
            if (json.success === "success") {
                console.log("Successfully add the review")

                // Can edit and delete
                var buttonsHtml = '';

                buttonsHtml += `<div class="review-actions">
                <a href="edit-review/${json.review_id}/" class="review-edit-btn">Edit</a>
                <form method="post" action="delete-review/${json.review_id}/">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                    <button type="submit" class="review-delete-btn">Delete</button>
                </form>
                </div>`;


                var newReviewHtml = `
                    <div class="comment">
                        <div class="review-header">
                            <h3>${json.title}</h3>
                            <p>★ ${json.rating}</p>
                        </div>
                        <p>${json.content}</p>
                        <p>Just now</p>
                        <p>Reviewed by: ${json.author}</p>
                        ${buttonsHtml}
                    </div>
        `;

                // $('.review-section').append(newReviewHtml);
                $('.review-section').prepend(newReviewHtml);

            } else {
                console.log("Error: " + json.error)
            }

        }).fail(function (xhr, status, errorThrown) {
            console.log("Sorry, there was a problem!")
            console.log("Error: " + errorThrown);
        }).always(function (xhr, status) {
            console.log("The request is complete!");
        })

    })

    // Delete
    $(document).on('click', '.delete-btn', function () {
        // console.log("Delete button clicked");
        // var reviewId = $(this).closest('.comment').data('id');
        // if (confirm('Are you sure you want to delete this review?')) {
        //     $.ajax({
        //         url: '/delete-review/' + reviewId,
        //         type: 'DELETE',
        //         headers: {"X-CSRFToken": csrftoken},
        //         success: function (result) {
        //             $('div[data-id="' + reviewId + '"]').remove();
        //         },
        //         error: function (xhr, status, error) {
        //             alert('Error: ' + error);
        //         }
        //     });
        // }
    });

})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');