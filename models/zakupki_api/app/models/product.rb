class Product < ApplicationRecord
  belongs_to :category
  has_many :properties, through: :category
end
