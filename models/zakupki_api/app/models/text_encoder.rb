require 'httparty'

class TextEncoder
  include HTTParty
  base_uri ENV.fetch('ENCODER_URL')

  def self.encode_text(text)
    response = post('/encode', body: { text: text }.to_json, headers: { 'Content-Type' => 'application/json' })
    if response.success?
      response.parsed_response
    else
      { error: "Failed to encode text: #{response.message}" }
    end
  end
end
