# frozen_string_literal: true

class CreateProducts < ActiveRecord::Migration[7.1]
  def change
    execute <<~SQL
        CREATE EXTENSION IF NOT EXISTS lantern;
        CREATE TABLE products (id bigint, name text, image text,  category_id bigint, category_name text, model text, vendor text, name_vector real[768], created_at timestamp, updated_at timestamp, PRIMARY KEY(id));
    SQL
  end
end
