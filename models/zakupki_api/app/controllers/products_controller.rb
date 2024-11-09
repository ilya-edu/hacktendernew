class ProductsController < ApplicationController

  BASE_LIMIT = 10
  def index
    encoded_text = TextEncoder.encode_text(q)
    attributes = "id, name, image, category_id, category_name, model, vendor"
    @products = Product.find_by_sql(["SELECT #{attributes} FROM products WHERE name_tsvector @@ plainto_tsquery('russian', ?) ORDER BY name_vector <=> ? LIMIT #{BASE_LIMIT}",q, encoded_text])
    if @products.size < 10
      additional_load_count = BASE_LIMIT - @products.size
      @products += Product.find_by_sql(["SELECT #{attributes} FROM products WHERE name_tsvector @@ plainto_tsquery('russian', ?) ORDER BY name_vector <=> ? LIMIT #{additional_load_count}", q.first(10), encoded_text])
    end
  end

  def models
    @models = Product.select("DISTINCT model").where("model ilike ?", "%#{q}%").limit(100)
  end
  def vendors
    @vendors = Product.select("DISTINCT vendor").where("vendor ilike ?", "%#{q}%").limit(100)
  end
  def q
    params.require(:q)
  end
end
