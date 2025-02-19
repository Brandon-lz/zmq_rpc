package main

import (
	"encoding/json"
	"fmt"
	"time"

	"gorm.io/datatypes"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type OperatorLogs struct {
	ID               uint      `gorm:"primaryKey;autoIncrement"`
	WorkerName       string    `gorm:"column:worker_name;index;"`
	WorkerId         string    `gorm:"column:worker_id;size:512;"`
	ClassGroup       string    `gorm:"column:class_group;size:512;"`
	OperationTime    time.Time `gorm:"column:operation_time;size:512;"`
	OperationYear    int       `gorm:"column:operation_year"`
	OperationMonth   int       `gorm:"column:operation_month"`
	OperationDay     int       `gorm:"column:operation_day"`
	OperationType    string    `gorm:"column:operation_type;size:512;"`
	OperationContent string    `gorm:"column:operation_content;"`
	OperationResult  string    `gorm:"column:operation_result;size:512;"`
}

func (OperatorLogs) TableName() string {
	return "operatorlogs"
}

type System struct {
	ID       uint           `gorm:"primaryKey;autoIncrement"`
	Version  string         `gorm:"column:version;size:512;"`
	Settings datatypes.JSON `gorm:"column:settings;size:512;"`
	CreateAt time.Time      `gorm:"column:create_at;size:512;"`
}

func (System) TableName() string {
	return "system"
}

type User struct {
	ID           uint      `gorm:"primaryKey;autoIncrement"`
	Name         string    `gorm:"column:name;size:512;"`
	WorkerId     string    `gorm:"column:worker_id;size:512;uniqueIndex;"`
	ClassGroup   string    `gorm:"column:class_group;size:512;"`
	Password     string    `gorm:"column:password;size:512;"`
	FacePath     string    `gorm:"column:face_path;size:512;"`
	IsSuperuser bool      `gorm:"column:is_superuser;size:512;"`
	Created_at   time.Time `gorm:"column:created_at;size:512;"`
}

func (User) TableName() string {
	return "user"
}


type ProcessSet struct {
	ID           uint      `gorm:"primaryKey;autoIncrement"`
	Value string      `gorm:"column:values;"`
	Created_at   time.Time `gorm:"column:created_at;"`
}

func (ProcessSet) TableName() string {
	return "process_set"
}

func main() {
	dsn := "host=localhost user=postgres password=postgres dbname=postgres port=5432 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{}, &gorm.Config{})
	if err != nil {
		panic(err)
	}

	err = db.AutoMigrate(&OperatorLogs{}, &System{}, &User{}, &ProcessSet{})
	if err != nil {
		panic(err)
	}

	err = db.Save(&User{Name: "admin", Password: "123456", WorkerId: "-1", ClassGroup: "-1", IsSuperuser: true, Created_at: time.Now()}).Error
	if err != nil {
		panic(err)
	}
	err = db.Save(&User{Name: "马金山", Password: "123456", WorkerId: "10001", ClassGroup: "1", IsSuperuser: false, Created_at: time.Now()}).Error
	if err != nil {
		panic(err)
	}
	system := System{Version: "1.0.0", CreateAt: time.Now()}
	settings := make(map[string]interface{})
	settings["open_log_record"] = true
	d, err := json.Marshal(settings)
	if err != nil {
		panic(err)
	}
	err = system.Settings.Scan(d)
	if err != nil {
		panic(err)
	}
	fmt.Println(system)

	err = db.Save(&system).Error
	if err != nil {
		panic(err)
	}
}

// CGO_ENABLED=0 go build .
