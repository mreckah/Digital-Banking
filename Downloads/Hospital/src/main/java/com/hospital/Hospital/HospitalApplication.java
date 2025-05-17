package com.hospital.Hospital;

import com.hospital.Hospital.entities.Patient;
import com.hospital.Hospital.repository.PatientRepo;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.text.SimpleDateFormat;
import java.util.Date;

@SpringBootApplication
public class HospitalApplication {
	public static void main(String[] args) {
		SpringApplication.run(HospitalApplication.class, args);
	}

	@Bean
	CommandLineRunner initDatabase(PatientRepo patientRepository) {
		return args -> {
			SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");

			Patient p1 = new Patient(0, "Oussama", sdf.parse("1995-04-12"), "Flu", 85);
			Patient p2 = new Patient(0, "mreckah", sdf.parse("1980-07-22"), "Diabetes", 72);
			Patient p3 = new Patient(0, "NABBAR", sdf.parse("1975-09-10"), "Hypertension", 90);
			Patient p4 = new Patient(0, "Oussama", sdf.parse("1995-04-12"), "Flu", 85);
			Patient p5 = new Patient(0, "mreckah", sdf.parse("1980-07-22"), "Diabetes", 72);
			Patient p7 = new Patient(0, "NABBAR", sdf.parse("1975-09-10"), "Hypertension", 90);

			patientRepository.save(p1);
			patientRepository.save(p2);
			patientRepository.save(p3);
			patientRepository.save(p4);
			patientRepository.save(p5);
			patientRepository.save(p7);

			System.out.println("✅ 3 patients added successfully!");
		};
	}
}
