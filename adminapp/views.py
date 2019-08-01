from django.shortcuts import render, get_object_or_404
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UsersListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'

        return context


class UsersCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(UsersCreateView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/создание'

        return context


class UsersUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin:users')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(UsersUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'пользователи/редактирование'

        return context


class UsersDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoriesListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(CategoriesListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CategoriesListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/категории'

        return context


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'категории/создание'

        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 3

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductsListView, self).dispatch(*args, **kwargs)


    def get(self, request, **kwargs):
        if request.is_ajax():
            quantity = int(self.kwargs["quantity"])
            new_product_item = get_object_or_404(Product, pk=int(self.kwargs["pk"]))
            if quantity > 0:
                new_product_item.quantity = quantity
                new_product_item.is_active = True
                new_product_item.save()
            else:
                new_product_item.quantity = quantity
                new_product_item.is_active = False
                new_product_item.save()

            self.object_list = self.get_queryset()
            context = super(ProductsListView, self).get_context_data(**kwargs)
            context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs["category_pk"])

            result = render_to_response('basketapp/includes/inc_product_quantity.html', context)
            return JsonResponse({'result': result})

        return super(ProductsListView, self).get(request, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/продукт'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs["pk"])

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/products_update.html'
    success_url = reverse_lazy('admin:products')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'продукт/создание'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs["pk"])

        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/products_update.html'
    success_url = reverse_lazy('admin:product_update')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        edit_product = get_object_or_404(Product, pk=self.kwargs["pk"])
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        context['category'] = edit_product.category

        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/products_delete.html'
    success_url = reverse_lazy('admin:products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(ProductDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        context['category'] = get_object_or_404(ProductCategory, pk=self.kwargs["pk"])

        return context