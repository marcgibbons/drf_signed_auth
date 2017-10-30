from rest_framework_csv.renderers import CSVRenderer


class PaginatedCSVRenderer(CSVRenderer):
    results_field = 'results'

    def render(
            self,
            data,
            media_type=None,
            renderer_context=None,
            writer_opts=None
    ):
        if not isinstance(data, list):
            data = data.get(self.results_field, [])

        filename = renderer_context['view'] \
            .get_view_name().replace(' ', '_').lower()

        renderer_context['response']['Content-Disposition'] =  \
            f'attachment; filename="{filename}.csv"'

        return super().render(data, media_type, renderer_context, writer_opts)
