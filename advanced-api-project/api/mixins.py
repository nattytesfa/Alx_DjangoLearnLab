from rest_framework import status
from rest_framework.response import Response


class CustomCreateMixin:
    """
    Custom mixin to enhance create operations.
    """
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Custom response with additional data
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'status': 'success',
                'message': 'Resource created successfully',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class CustomUpdateMixin:
    """
    Custom mixin to enhance update operations.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Custom response
        return Response(
            {
                'status': 'success',
                'message': 'Resource updated successfully',
                'data': serializer.data
            }
        )


class CustomDestroyMixin:
    """
    Custom mixin to enhance delete operations.
    """
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        # Custom response for delete
        return Response(
            {
                'status': 'success',
                'message': 'Resource deleted successfully'
            },
            status=status.HTTP_204_NO_CONTENT
        )
