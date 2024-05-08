from django.contrib import admin
from .models import Clothes, Comment, ImageClothes, SizeClothes
from django.contrib.admin import SimpleListFilter
# Register your models here.

class SizeClothesClothesFilter(SimpleListFilter):
    title = 'Producto'  # El título que aparecerá en el filtro
    parameter_name = 'clothes'  # El parámetro usado en la URL

    def lookups(self, request, model_admin):
        # Obtener todas las prendas únicas para usar como opciones de filtro
        clothes = set(SizeClothes.objects.values_list('color_clothe__clothes__name', flat=True))
        return [(clothe, clothe) for clothe in clothes]

    def queryset(self, request, queryset):
        # Filtrar el queryset basado en la selección del filtro
        if self.value():
            return queryset.filter(color_clothe__clothes__name=self.value())
        return queryset

class ClothesAdmin(admin.ModelAdmin):
    list_filter = ("type", "gender", )
    list_display = ("name", "type", "gender",)
    prepopulated_fields = {"slug": ("name",)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "clothes", "date", "rating",)

class ImageClothesAdmin(admin.ModelAdmin):
    list_display = ('color', 'clothes',)
    list_filter = ("clothes", )

class SizeClothesAdmin(admin.ModelAdmin):
     list_display = ('size', 'cant', 'color_clothe', 'clothes')
     list_filter = (SizeClothesClothesFilter, 'color_clothe', 'size', 'in_stock',)  # Usar el filtro personalizado
     search_fields = ('size', 'color_clothe__name', 'color_clothe__clothes__name')  # Hacer buscable

     def clothes(self, obj):
        return obj.color_clothe.clothes.name


admin.site.register(Clothes, ClothesAdmin)
admin.site.register(ImageClothes, ImageClothesAdmin)
admin.site.register(SizeClothes, SizeClothesAdmin)
admin.site.register(Comment, CommentAdmin)
