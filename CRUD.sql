CREATE OR REPLACE FUNCTION update_bike_availability() RETURNS TRIGGER AS $$
BEGIN
  UPDATE bike_infos SET availability = FALSE WHERE bike_id = NEW.rent_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER change_availability
AFTER INSERT ON customer_infos
FOR EACH ROW
EXECUTE FUNCTION update_bike_availability();


CREATE OR REPLACE FUNCTION reset_bike_availability() RETURNS TRIGGER AS $$
BEGIN
  UPDATE bike_infos SET availability = TRUE WHERE bike_id = OLD.rent_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER reset_availability 
AFTER DELETE ON customer_infos
FOR EACH ROW
EXECUTE FUNCTION reset_bike_availability();

