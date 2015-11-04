/**
 * Created by snake on 2015-11-02.
 */

$(function () {
    $('.sorted-autocomplete-m2m').each(function (__, main_container) {
        main_container = $(main_container);
        var field_name = main_container.attr('data-name');
        var autocomplete_input = main_container.find('input[data-autocomplete-url]');
        var autocomplete_url = autocomplete_input.attr('data-autocomplete-url');
        var autocomplete_results = main_container.find('.autocomplete-results');
        var autocomplete_results_container = main_container.find('.autocomplete-results-container');
        var sorted_results = main_container.find('.sortedm2m-results');
        var ajax_timeout;

        autocomplete_input.keyup(function (event) {
            if (event.keyCode == 13) {
                event.preventDefault();
                // tODO: select first in list
            }
            var q = autocomplete_input.val();
            if (!q) {
                autocomplete_clear();
                return;
            }
            clearTimeout(ajax_timeout);
            ajax_timeout = setTimeout(function () {
                $.get(autocomplete_url, {q: q}, function (result) {
                    var choices = result['choices'];
                    if (choices) {
                        autocomplete_results.html('');
                        autocomplete_results_container.show();
                        for (var i = 0; i < choices.length; i++)
                            autocomplete_add(choices[i].id, choices[i].value);
                    }
                });
            }, 100);
        });

        function autocomplete_add(id, value) {
            var element_id = 'id_autocomplete_' + field_name + '_' + id;
            var element_html = '<li id="' + element_id + '">' + value + '</li>';
            autocomplete_results.append(element_html);
            var element = $('#' + element_id);
            element.click(function (e) {
                sorted_add(id, value);
                autocomplete_clear();
                autocomplete_input.val('');
            })
        }

        function autocomplete_clear() {
            autocomplete_results.html('');
            autocomplete_results_container.hide();
        }

        function sorted_add(id, value) {
            var element_id = 'id_sorted_' + field_name + '_' + id;
            var element_html = '' +
                '<li id="' + element_id + '">' +
                '<label for="' + element_id + '_label">' +
                '<input class="sortedm2m" id="' + element_id + '_label" ' +
                '  type="checkbox" value="' + id + '"> ' + value +
                '</label>' +
                '</li>';
            sorted_results.append(element_html);
            $('#' +  element_id + '_label').click();
        }
    });
});