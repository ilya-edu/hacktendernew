json.extract! product, :id, :name, :image, :model, :vendor
json.category do
  json.partial! product.category, partial: "categories/category", as: :category
end