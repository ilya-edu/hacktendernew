class PropertiesController < ApplicationController

  def index
    encoded_text = TextEncoder.encode_text(q)
    attributes = "id, name, category_id, category_name, kind"
    @properties = Property.find_by_sql(["SELECT #{attributes} FROM properties WHERE category_id in (?) ORDER BY name_vector <=> ? LIMIT 100", category_ids.split(",") , encoded_text])
  end
  def q
    params.required(:q)
  end
  def category_ids
    params.required(:category_ids)
  end
end
