class CategoriesController < ApplicationController
  def index
    @categories = Category.where("name_tsvector @@ plainto_tsquery('russian', ?) ", q).limit(limit).offset(offset)
  end
  def show
    @category = Category.find(params[:id])
  end

  def limit
    params[:limit] || 50
  end
  def offset
    params[:offset] || 0
  end
  def q
    params[:q]
  end
end
